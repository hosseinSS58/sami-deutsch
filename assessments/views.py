from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, FormView
from django.db.models import Prefetch
import re
import time
from .models import Assessment, Question, Choice, Submission, SubmissionItem
from .forms import build_assessment_form


def user_identifier_for_request(request) -> str:
    if request.user.is_authenticated:
        return f"user-{request.user.id}"
    if not request.session.session_key:
        request.session.create()
    return f"anon-{request.session.session_key}"


class AssessmentIntroView(TemplateView):
    template_name = "assessments/intro.html"

    def get(self, request, *args, **kwargs):
        active_assessments = Assessment.objects.filter(is_active=True)
        if active_assessments.count() == 1:
            # If only one assessment, go to classic mode for it
            request.session["assessment_id"] = active_assessments.first().id
            request.session["adaptive"] = False
            return redirect("assessments:take")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        active_assessments = Assessment.objects.filter(is_active=True).order_by("level", "title")
        ctx["levels_available"] = sorted(set(active_assessments.values_list("level", flat=True)))
        ctx["assessments"] = active_assessments
        return ctx


class AssessmentTakeView(FormView):
    template_name = "assessments/take.html"
    form_class = None
    started_initial = False

    def _get_user_identifier(self) -> str:
        # Ensure stable identifier per user/guest
        return user_identifier_for_request(self.request)

    def _attempts_exceeded(self) -> bool:
        limit = getattr(self.assessment, "attempt_limit", 0) or 0
        if limit <= 0:
            return False
        user_identifier = self._get_user_identifier()
        attempt_count = Submission.objects.filter(
            assessment=self.assessment,
            user_identifier=user_identifier,
        ).count()
        return attempt_count >= limit

    def _cache_elapsed(self) -> int:
        start_ts = int(self.request.session.get("assessment_start", int(time.time())))
        elapsed = max(0, int(time.time()) - start_ts)
        self._elapsed_seconds_cache = elapsed
        return elapsed

    def _time_limit_exceeded(self) -> bool:
        limit = getattr(self.assessment, "time_limit_seconds", 0) or 0
        if limit <= 0:
            return False
        elapsed = self._cache_elapsed()
        return elapsed > limit

    def _reset_assessment_progress(self):
        keys = ["assessment_start", "adaptive_state", "adaptive_history", "identity"]
        for key in keys:
            self.request.session.pop(key, None)
        # Keep the current mode; default to adaptive if not set
        self.request.session["adaptive"] = self.request.session.get("adaptive", True)

    def dispatch(self, request, *args, **kwargs):
        # Determine mode
        mode = request.GET.get("mode")
        if mode == "classic":
            request.session["adaptive"] = False
        elif mode == "adaptive":
            request.session["adaptive"] = True
        else:
            # If no explicit mode is provided, default to adaptive
            request.session.setdefault("adaptive", True)
            # If a previous classic run forced non-adaptive, reset to adaptive when starting fresh
            if request.session.get("adaptive") is False and not request.session.get("adaptive_state") and not request.GET.get("assessment_id"):
                request.session["adaptive"] = True
                request.session.pop("assessment_id", None)

        adaptive = request.session.get("adaptive", True)

        # Classic mode: allow explicit assessment selection
        assessment_id = request.GET.get("assessment_id") or request.session.get("assessment_id")
        if not adaptive:
            # fallback to first active assessment if none specified
            if not assessment_id:
                first_assessment = Assessment.objects.filter(is_active=True).order_by("id").first()
                if first_assessment:
                    assessment_id = first_assessment.id
            if not assessment_id:
                messages.error(request, _("هیچ آزمون فعالی یافت نشد."))
                return redirect("assessments:intro")
            self.assessment = get_object_or_404(Assessment, id=assessment_id, is_active=True)
            request.session["assessment_id"] = self.assessment.id
            media_qs = self.assessment.questions.model.media_items.rel.related_model.objects.order_by("order", "id")
            self.questions = list(
                self.assessment.questions.order_by("id").prefetch_related(
                    "choices",
                    "answer_patterns",
                    "ordering_items",
                    "match_pairs",
                    Prefetch("media_items", queryset=media_qs),
                )
            )
            self.form_class = build_assessment_form(self.assessment, questions=self.questions, user=request.user)
            if self._attempts_exceeded():
                messages.warning(self.request, _("به حداکثر دفعات مجاز برای این آزمون رسیده‌اید."))
                return redirect("assessments:result")
            if self._time_limit_exceeded():
                self._reset_assessment_progress()
                messages.info(self.request, _("مهلت آزمون قبلی شما تمام شد. می‌توانید دوباره شروع کنید."))
                return redirect("assessments:take")
            # authenticated users skip identity
            if request.user.is_authenticated and not request.session.get("identity"):
                request.session["identity"] = {
                    "full_name": request.user.get_full_name() or request.user.username,
                    "email": request.user.email,
                }
            ident = request.session.get("identity", {})
            self.started_initial = bool(ident.get("full_name") and ident.get("email")) or request.user.is_authenticated
            request.session.setdefault("assessment_start", int(time.time()))
            return super().dispatch(request, *args, **kwargs)

        # Adaptive mode (default)
        level_order = ["A1", "A2", "B1", "B2"]
        level_batch_sizes = {"A1": 5, "A2": 7, "B1": 9, "B2": 12}

        request.session["adaptive"] = True
        # Clear any previous classic assessment selection to avoid sticking to a fixed test
        request.session.pop("assessment_id", None)
        if "adaptive_state" not in request.session:
            request.session["adaptive_state"] = {
                "current_level": "A1",
                "asked_by_level": {lvl: [] for lvl in level_order},
                "start_ts": int(time.time()),
            }
            request.session["adaptive_history"] = []
        state = request.session["adaptive_state"]
        current_level = state.get("current_level", "A1")

        self.assessment = get_object_or_404(Assessment, level=current_level, is_active=True)

        asked_ids = set(state.get("asked_by_level", {}).get(current_level, []))
        qs = (
            self.assessment.questions.order_by("id")
            .prefetch_related(
                "choices",
                "answer_patterns",
                "ordering_items",
                "match_pairs",
                Prefetch("media_items", queryset=self.assessment.questions.model.media_items.rel.related_model.objects.order_by("order", "id")),
            )
        )
        batch = []
        batch_size = level_batch_sizes.get(current_level, 5)
        for q in qs:
            if q.id not in asked_ids:
                batch.append(q)
            if len(batch) >= batch_size:
                break
        if not batch:
            batch = list(qs[:batch_size])

        self.questions = batch
        self.form_class = build_assessment_form(self.assessment, questions=batch, user=request.user)
        if self._attempts_exceeded():
            messages.warning(self.request, _("به حداکثر دفعات مجاز برای این آزمون رسیده‌اید."))
            return redirect("assessments:result")
        if self._time_limit_exceeded():
            self._reset_assessment_progress()
            messages.info(self.request, _("مهلت آزمون قبلی شما تمام شد. می‌توانید دوباره شروع کنید."))
            return redirect("assessments:take")
        # Identity handling
        if request.user.is_authenticated:
            request.session["identity"] = {
                "full_name": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
            }
        ident = request.session.get("identity", {})
        self.started_initial = bool(ident.get("full_name") and ident.get("email")) or request.user.is_authenticated
        request.session.setdefault("assessment_start", state.get("start_ts", int(time.time())))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get("form")
        if form is not None:
            # Group fields by question id to support multi-input cloze rendering
            groups = []
            for q in getattr(self, "questions", []):
                base = f"q_{q.id}"
                q_fields = []
                for f in form:
                    name = str(getattr(f, "name", ""))
                    if name == base or name.startswith(f"{base}_blank_"):
                        q_fields.append(f)
                if q_fields:
                    groups.append(
                        {
                            "question": q,
                            "fields": q_fields,
                            "media": list(getattr(q, "media_items", []).all()) if hasattr(q, "media_items") else [],
                        }
                    )
            context["question_groups"] = groups
            context["question_fields"] = [f for f in form if str(getattr(f, "name", "")).startswith("q_")]
        context["time_limit"] = self.assessment.time_limit_seconds
        # Adaptive identity form toggle
        has_identity = bool(
            self.request.user.is_authenticated
            or (self.request.session.get("identity", {}).get("full_name") and self.request.session.get("identity", {}).get("email"))
        )
        context["show_identity_form"] = not has_identity
        context["started_initial"] = self.started_initial
        return context

    def form_valid(self, form):
        if self._time_limit_exceeded():
            self._reset_assessment_progress()
            messages.warning(self.request, _("مهلت آزمون به پایان رسیده است. لطفاً دوباره شروع کنید."))
            return redirect("assessments:take")
        if self._attempts_exceeded():
            form.add_error(None, _("به حداکثر دفعات مجاز برای این آزمون رسیده‌اید."))
            return self.form_invalid(form)
        # Classic single-assessment mode
        if not self.request.session.get("adaptive"):
            total_weight = 0
            gained_total = 0.0
            elapsed = getattr(self, "_elapsed_seconds_cache", None)
            if elapsed is None:
                elapsed = self._cache_elapsed()
            submission = Submission.objects.create(
                assessment=self.assessment,
                user_identifier=self._get_user_identifier(),
                full_name=self.request.user.get_full_name() or form.cleaned_data.get("full_name", ""),
                email=self.request.user.email if self.request.user.is_authenticated else form.cleaned_data.get("email", ""),
            )
            for question in self.questions:
                field = form.cleaned_data.get(f"q_{question.id}")
                is_correct = False
                gained = 0.0
                if question.type == Question.QuestionType.MCQ_SINGLE:
                    selected_id = int(field)
                    is_correct = any(c.id == selected_id and c.is_correct for c in question.choices.all())
                    gained = question.weight if is_correct else 0.0
                    SubmissionItem.objects.create(
                        submission=submission,
                        question=question,
                        selected_choice_id=selected_id,
                        is_correct=is_correct,
                        gained_score=gained,
                    )
                elif question.type == Question.QuestionType.MULTI:
                    selected_ids = [int(x) for x in (field or [])]
                    correct_ids = set(question.choices.filter(is_correct=True).values_list("id", flat=True))
                    is_correct = set(selected_ids) == correct_ids
                    # partial credit
                    if correct_ids:
                        overlap = len(correct_ids.intersection(selected_ids)) / len(correct_ids)
                    else:
                        overlap = 0.0
                    gained = question.weight * overlap
                    SubmissionItem.objects.create(
                        submission=submission,
                        question=question,
                        is_correct=is_correct,
                        gained_score=gained,
                    )
                elif question.type == Question.QuestionType.TF:
                    val = str(field)
                    expected = "true" if question.correct_boolean else "false"
                    is_correct = val == expected
                    gained = question.weight if is_correct else 0.0
                    SubmissionItem.objects.create(
                        submission=submission,
                        question=question,
                        is_correct=is_correct,
                        gained_score=gained,
                    )
                elif question.type == Question.QuestionType.FILL:
                    text = str(field or "").strip()
                    # Evaluate against patterns
                    for p in question.answer_patterns.all():
                        if p.kind == p.PatternType.EXACT and text == p.pattern:
                            is_correct = True
                            break
                        if p.kind == p.PatternType.ICASE and text.lower() == p.pattern.lower():
                            is_correct = True
                            break
                        if p.kind == p.PatternType.REGEX and re.fullmatch(p.pattern, text):
                            is_correct = True
                            break
                    gained = question.weight if is_correct else 0.0
                    SubmissionItem.objects.create(
                        submission=submission,
                        question=question,
                        user_text=text,
                        is_correct=is_correct,
                        gained_score=gained,
                    )
                elif question.type == Question.QuestionType.ORDER:
                    order_str = str(field or "").replace(" ", "")
                    try:
                        ids = [int(x) for x in order_str.split(",") if x]
                    except ValueError:
                        ids = []
                    correct_order = list(question.ordering_items.order_by("correct_position").values_list("id", flat=True))
                    is_correct = ids == correct_order
                    # Kendall tau-like partial credit
                    gained = 0.0
                    if correct_order and ids:
                        matched = sum(1 for a, b in zip(ids, correct_order) if a == b)
                        gained = question.weight * (matched / len(correct_order))
                    SubmissionItem.objects.create(
                        submission=submission,
                        question=question,
                        user_text=order_str,
                        is_correct=is_correct,
                        gained_score=gained,
                    )
                elif question.type == Question.QuestionType.MATCH:
                    lines = str(field or "").splitlines()
                    pairs = {}
                    for ln in lines:
                        if "=" in ln:
                            l, r = ln.split("=", 1)
                            pairs[l.strip()] = r.strip()
                    correct_pairs = {p.left_text: p.right_text for p in question.match_pairs.all()}
                    correct_count = sum(1 for k, v in correct_pairs.items() if pairs.get(k) == v)
                    gained = question.weight * (correct_count / max(len(correct_pairs), 1))
                    is_correct = correct_count == len(correct_pairs) and len(correct_pairs) > 0
                    SubmissionItem.objects.create(
                        submission=submission,
                        question=question,
                        user_text=";".join(f"{k}={v}" for k, v in pairs.items()),
                        is_correct=is_correct,
                        gained_score=gained,
                    )
                total_weight += question.weight
                gained_total += gained

            duration = elapsed
            ratio = gained_total / max(total_weight, 1)
            thresholds = [
                (0.75, "B2"),
                (0.55, "B1"),
                (0.35, "A2"),
                (0.0, "A1"),
            ]
            recommended = next(level for th, level in thresholds if ratio >= th)
            submission.score = float(gained_total)
            submission.total_weight = float(total_weight)
            submission.ratio = float(ratio)
            submission.duration_seconds = duration
            submission.recommended_level = recommended
            submission.save(update_fields=["score", "recommended_level"])
            # persist enhanced fields
            submission.save(update_fields=["total_weight", "ratio", "duration_seconds"]) 
            # increment attempts
            attempts = self.request.session.get("attempts", {})
            attempts[str(self.assessment.id)] = attempts.get(str(self.assessment.id), 0) + 1
            self.request.session["attempts"] = attempts
            self.request.session["recommended_level"] = recommended
            return redirect("assessments:result")

        # Adaptive mode: grade current batch, choose next level or finalize
        state = self.request.session.get("adaptive_state", {})
        current_level = state.get("current_level", "A1")
        level_order = ["A1", "A2", "B1", "B2"]

        # Score this batch only
        batch_total = 0.0
        batch_gained = 0.0
        correct_full = 0
        for question in self.questions:
            field = form.cleaned_data.get(f"q_{question.id}")
            is_correct = False
            gained = 0.0
            if question.type == Question.QuestionType.MCQ_SINGLE:
                selected_id = int(field)
                is_correct = any(c.id == selected_id and c.is_correct for c in question.choices.all())
                gained = question.weight if is_correct else 0.0
            elif question.type == Question.QuestionType.MULTI:
                selected_ids = [int(x) for x in (field or [])]
                correct_ids = set(question.choices.filter(is_correct=True).values_list("id", flat=True))
                is_correct = set(selected_ids) == correct_ids
                # partial credit
                if correct_ids:
                    overlap = len(correct_ids.intersection(selected_ids)) / len(correct_ids)
                else:
                    overlap = 0.0
                gained = question.weight * overlap
            elif question.type == Question.QuestionType.TF:
                val = str(field)
                expected = "true" if question.correct_boolean else "false"
                is_correct = val == expected
                gained = question.weight if is_correct else 0.0
            elif question.type == Question.QuestionType.FILL:
                text = str(field or "").strip()
                # Evaluate against patterns
                for p in question.answer_patterns.all():
                    if p.kind == p.PatternType.EXACT and text == p.pattern:
                        is_correct = True
                        break
                    if p.kind == p.PatternType.ICASE and text.lower() == p.pattern.lower():
                        is_correct = True
                        break
                    if p.kind == p.PatternType.REGEX and re.fullmatch(p.pattern, text):
                        is_correct = True
                        break
                gained = question.weight if is_correct else 0.0
            elif question.type == Question.QuestionType.ORDER:
                order_str = str(field or "").replace(" ", "")
                try:
                    ids = [int(x) for x in order_str.split(",") if x]
                except ValueError:
                    ids = []
                correct_order = list(question.ordering_items.order_by("correct_position").values_list("id", flat=True))
                is_correct = ids == correct_order
                # Kendall tau-like partial credit
                gained = 0.0
                if correct_order and ids:
                    matched = sum(1 for a, b in zip(ids, correct_order) if a == b)
                    gained = question.weight * (matched / len(correct_order))
            elif question.type == Question.QuestionType.MATCH:
                # If multi-blank inputs exist, reconstruct pairs from them; else parse textarea
                pairs = {}
                # Collect per-blank inputs
                for name, val in form.cleaned_data.items():
                    if isinstance(name, str) and name.startswith(f"q_{question.id}_blank_"):
                        left = name.split(f"q_{question.id}_blank_")[1]
                        pairs[left.strip()] = str(val or "").strip()
                if not pairs:
                    lines = str(field or "").splitlines()
                    for ln in lines:
                        if "=" in ln:
                            l, r = ln.split("=", 1)
                            pairs[l.strip()] = r.strip()
                correct_pairs = {p.left_text: p.right_text for p in question.match_pairs.all()}
                correct_count = sum(1 for k, v in correct_pairs.items() if pairs.get(k) == v)
                gained = question.weight * (correct_count / max(len(correct_pairs), 1))
                is_correct = correct_count == len(correct_pairs) and len(correct_pairs) > 0
            batch_total += question.weight
            batch_gained += gained
            if abs(gained - question.weight) < 1e-9:
                correct_full += 1

        # Persist identity from first batch
        if self.request.session.get("adaptive") and not self.request.session.get("identity"):
            full_name = form.cleaned_data.get("full_name", "").strip()
            email = form.cleaned_data.get("email", "").strip()
            if full_name and email:
                self.request.session["identity"] = {"full_name": full_name, "email": email}

        # Update asked list
        asked_by_level = state.get("asked_by_level", {})
        already = set(asked_by_level.get(current_level, []))
        already.update(q.id for q in self.questions)
        asked_by_level[current_level] = list(already)
        state["asked_by_level"] = asked_by_level

        # Decide next level based on ratio thresholds
        ratio = batch_gained / max(batch_total, 1.0)
        # Build per-question detail for later reporting
        detail = []
        for question in self.questions:
            # Re-evaluate quickly to capture boolean per question
            field = form.cleaned_data.get(f"q_{question.id}")
            q_correct = False
            if question.type == Question.QuestionType.MCQ_SINGLE:
                try:
                    selected_id = int(field)
                except (TypeError, ValueError):
                    selected_id = -1
                q_correct = any(c.id == selected_id and c.is_correct for c in question.choices.all())
            elif question.type == Question.QuestionType.MULTI:
                selected_ids = set(int(x) for x in (field or []))
                correct_ids = set(question.choices.filter(is_correct=True).values_list("id", flat=True))
                q_correct = selected_ids == correct_ids
            elif question.type == Question.QuestionType.TF:
                val = str(field)
                expected = "true" if question.correct_boolean else "false"
                q_correct = (val == expected)
            elif question.type == Question.QuestionType.FILL:
                text = str(field or "").strip()
                for p in question.answer_patterns.all():
                    if p.kind == p.PatternType.EXACT and text == p.pattern:
                        q_correct = True
                        break
                    if p.kind == p.PatternType.ICASE and text.lower() == p.pattern.lower():
                        q_correct = True
                        break
                    if p.kind == p.PatternType.REGEX and re.fullmatch(p.pattern, text):
                        q_correct = True
                        break
            elif question.type == Question.QuestionType.ORDER:
                order_str = str(field or "").replace(" ", "")
                try:
                    ids = [int(x) for x in order_str.split(",") if x]
                except ValueError:
                    ids = []
                correct_order = list(question.ordering_items.order_by("correct_position").values_list("id", flat=True))
                q_correct = ids == correct_order
            elif question.type == Question.QuestionType.MATCH:
                pairs = {}
                for name, val in form.cleaned_data.items():
                    if isinstance(name, str) and name.startswith(f"q_{question.id}_blank_"):
                        left = name.split(f"q_{question.id}_blank_")[1]
                        pairs[left.strip()] = str(val or "").strip()
                if not pairs:
                    lines = str(field or "").splitlines()
                    for ln in lines:
                        if "=" in ln:
                            l, r = ln.split("=", 1)
                            pairs[l.strip()] = r.strip()
                correct_pairs = {p.left_text: p.right_text for p in question.match_pairs.all()}
                correct_count = sum(1 for k, v in correct_pairs.items() if pairs.get(k) == v)
                q_correct = (correct_count == len(correct_pairs) and len(correct_pairs) > 0)
            detail.append(
                {
                    "id": question.id,
                    "text": question.text,
                    "type_label": question.get_type_display(),
                    "correct": bool(q_correct),
                }
            )

        history = self.request.session.get("adaptive_history", [])
        history.append(
            {
                "level": current_level,
                "correct": int(correct_full),
                "total": len(self.questions),
                "ratio_percent": int(round(ratio * 100)),
                "questions": detail,
            }
        )
        self.request.session["adaptive_history"] = history
        # thresholds: <30% down, 30-60 stay, >60 up
        def level_index(lvl: str) -> int:
            try:
                return level_order.index(lvl)
            except ValueError:
                return 0

        idx = level_index(current_level)
        if ratio < 0.3 and idx > 0:
            next_level = level_order[idx - 1]
        elif 0.3 <= ratio <= 0.6:
            # finalize here
            next_level = current_level
            finalize = True
        else:
            # ratio > 0.6
            next_level = level_order[min(idx + 1, len(level_order) - 1)]

        finalize = locals().get("finalize", False)

        # Finalization conditions:
        # - If we stayed (30-60), finalize
        # - If we are at edges (A1 with <30 -> A1) or (B2 with >60 -> B2), finalize
        at_edge_and_finalize = (
            (current_level == "A1" and ratio < 0.3)
            or (current_level == "B2" and ratio > 0.6)
        )
        if at_edge_and_finalize:
            next_level = current_level
            finalize = True

        if finalize:
            # Create a single submission representing the recommended level
            elapsed = getattr(self, "_elapsed_seconds_cache", None)
            if elapsed is None:
                elapsed = self._cache_elapsed()
            submission = Submission.objects.create(
                assessment=self.assessment,  # store last used assessment
                user_identifier=self._get_user_identifier(),
                full_name=form.cleaned_data.get("full_name", ""),
                email=form.cleaned_data.get("email", ""),
                score=float(batch_gained),
                total_weight=float(batch_total),
                ratio=float(ratio),
                duration_seconds=elapsed,
                recommended_level=next_level,
            )
            # Minimal per-question items are not persisted in adaptive mode to keep DB lean
            self.request.session["recommended_level"] = next_level
            # Clear adaptive state
            self.request.session.pop("adaptive_state", None)
            self.request.session["adaptive"] = False
            return redirect("assessments:result")

        # Continue adaptive loop
        state["current_level"] = next_level
        self.request.session["adaptive_state"] = state
        return redirect("assessments:take")


class AssessmentResultView(TemplateView):
    template_name = "assessments/result.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["recommended_level"] = self.request.session.get("recommended_level")
        ctx["batch_history"] = list(self.request.session.get("adaptive_history", []))
        
        # Get the latest submission for this user
        user_identifier = user_identifier_for_request(self.request)
        submission_id = self.request.GET.get("submission_id")
        try:
            qs = Submission.objects.filter(user_identifier=user_identifier)
            if submission_id:
                latest_submission = qs.filter(id=submission_id).first()
            else:
                latest_submission = qs.order_by("-created_at").first()

            if latest_submission:
                ctx.update(
                    {
                        "submission": latest_submission,
                        "score": latest_submission.score,
                        "total_weight": latest_submission.total_weight,
                        "ratio": latest_submission.ratio,
                        "percentage": round(latest_submission.ratio * 100, 1) if latest_submission.total_weight else 0,
                        "duration_minutes": round(latest_submission.duration_seconds / 60, 1),
                        "recommended_level": latest_submission.recommended_level,
                        "created_at": latest_submission.created_at,
                    }
                )

                # Build incorrect questions hints (only for classic mode submissions with items)
                incorrect_details = []
                submission_items = list(
                    latest_submission.items.select_related("question").prefetch_related("question__hint_resources")
                )
                for item in submission_items:
                    if item.is_correct:
                        continue
                    q = item.question
                    incorrect_details.append(
                        {
                            "question": q,
                            "hint_text": q.hint_text,
                            "hint_links": q.hint_links or [],
                            "hint_resources": list(q.hint_resources.all()),
                        }
                    )
                ctx["incorrect_details"] = incorrect_details

                # Get recommended videos based on the user's level
                try:
                    from courses.models import Video

                    recommended_videos = (
                        Video.objects.filter(level=latest_submission.recommended_level)
                        .order_by("-is_featured", "-created_at")[:6]
                    )
                    ctx["recommended_videos"] = recommended_videos
                except ImportError:
                    ctx["recommended_videos"] = []

        except Submission.DoesNotExist:
            pass

        return ctx


# Create your views here.
