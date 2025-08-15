from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
import re
import time
from .models import Assessment, Question, Choice, Submission, SubmissionItem
from .forms import AssessmentStartForm, build_assessment_form


class AssessmentIntroView(FormView):
    template_name = "assessments/intro.html"
    form_class = AssessmentStartForm
    success_url = reverse_lazy("assessments:take")

    def form_valid(self, form):
        assessment = form.cleaned_data["assessment"]
        self.request.session["assessment_id"] = assessment.id
        return super().form_valid(form)


class AssessmentTakeView(FormView):
    template_name = "assessments/take.html"
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        assessment_id = request.session.get("assessment_id") or kwargs.get("assessment_id")
        self.assessment = get_object_or_404(Assessment, id=assessment_id, is_active=True)
        # Pick 20 mixed-type questions deterministically by id
        questions = list(
            self.assessment.questions
            .order_by("id")
            .prefetch_related("choices", "answer_patterns", "ordering_items", "match_pairs")[:20]
        )
        self.questions = questions
        self.form_class = build_assessment_form(self.assessment, questions=questions)
        # attempt limit control
        attempts = request.session.get("attempts", {}).get(str(self.assessment.id), 0)
        if attempts >= self.assessment.attempt_limit:
            return redirect("assessments:result")
        request.session.setdefault("assessment_start", int(time.time()))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get("form")
        if form is not None:
            context["question_fields"] = [f for f in form if str(getattr(f, "name", "")).startswith("q_")]
        context["time_limit"] = self.assessment.time_limit_seconds
        return context

    def form_valid(self, form):
        total_weight = 0
        gained_total = 0.0
        start_ts = int(self.request.session.get("assessment_start", int(time.time())))
        submission = Submission.objects.create(
            assessment=self.assessment,
            user_identifier=str(self.request.user.id or self.request.session.session_key),
            full_name=form.cleaned_data.get("full_name", ""),
            email=form.cleaned_data.get("email", ""),
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

        duration = max(0, int(time.time()) - start_ts)
        ratio = gained_total / max(total_weight, 1)
        thresholds = [
            (0.85, "C1"),
            (0.7, "B2"),
            (0.5, "B1"),
            (0.3, "A2"),
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


class AssessmentResultView(TemplateView):
    template_name = "assessments/result.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["recommended_level"] = self.request.session.get("recommended_level")
        return ctx


# Create your views here.
