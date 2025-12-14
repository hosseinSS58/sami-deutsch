from django.db import models
from django.utils.translation import gettext_lazy as _


class Assessment(models.Model):
    LEVEL_CHOICES = [
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C1", "C1"),
    ]
    title = models.CharField(max_length=150, verbose_name=_("عنوان"))
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, verbose_name=_("سطح پیشنهادی"))
    is_active = models.BooleanField(default=True)
    time_limit_seconds = models.PositiveIntegerField(default=600, verbose_name=_("مهلت پاسخ (ثانیه)"))
    attempt_limit = models.PositiveSmallIntegerField(default=3, verbose_name=_("حداکثر دفعات تلاش"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("آزمون تعیین سطح")
        verbose_name_plural = _("آزمون‌های تعیین سطح")

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    class QuestionType(models.TextChoices):
        MCQ_SINGLE = "mcq", _("چهارگزینه‌ای")
        MULTI = "multi", _("چندگزینه‌ای (چند پاسخ)")
        TF = "tf", _("درست/نادرست")
        FILL = "fill", _("جای خالی")
        ORDER = "order", _("ترتیب‌دهی")
        MATCH = "match", _("تطبیق")

    class Difficulty(models.TextChoices):
        EASY = "easy", _("ساده")
        MEDIUM = "medium", _("متوسط")
        HARD = "hard", _("سخت")

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=400, verbose_name=_("سوال"))
    type = models.CharField(max_length=10, choices=QuestionType.choices, default=QuestionType.MCQ_SINGLE)
    target_level = models.CharField(max_length=2, choices=Assessment.LEVEL_CHOICES, default="A1")
    difficulty = models.CharField(max_length=6, choices=Difficulty.choices, default=Difficulty.MEDIUM)
    weight = models.PositiveSmallIntegerField(default=1)
    explanation = models.TextField(blank=True)
    correct_boolean = models.BooleanField(null=True, blank=True, verbose_name=_("پاسخ صحیح (برای درست/نادرست)"))
    hint_text = models.TextField(blank=True, verbose_name=_("نکته/توضیح پس از پاسخ نادرست"))
    hint_links = models.JSONField(default=list, blank=True, verbose_name=_("لینک‌های پیشنهادی پس از پاسخ نادرست"))

    def __str__(self) -> str:
        return self.text[:50]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200, verbose_name=_("گزینه"))
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text[:50]


class AnswerPattern(models.Model):
    class PatternType(models.TextChoices):
        EXACT = "exact", _("مطابقت دقیق")
        ICASE = "icase", _("بدون حساسیت به حروف")
        REGEX = "regex", _("عبارت باقاعده")

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answer_patterns")
    pattern = models.CharField(max_length=200)
    kind = models.CharField(max_length=10, choices=PatternType.choices, default=PatternType.ICASE)

    def __str__(self) -> str:
        return f"{self.kind}:{self.pattern}"


class OrderingItem(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="ordering_items")
    text = models.CharField(max_length=200)
    correct_position = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["correct_position"]

    def __str__(self) -> str:
        return self.text


class MatchPair(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="match_pairs")
    left_text = models.CharField(max_length=200)
    right_text = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.left_text} ↔ {self.right_text}"


class QuestionMedia(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", _("تصویر")
        AUDIO = "audio", _("صوت")
        VIDEO = "video", _("ویدیو")
        TEXT = "text", _("متن")
        FILE = "file", _("فایل")

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="media_items")
    media_type = models.CharField(max_length=10, choices=MediaType.choices, default=MediaType.IMAGE)
    file = models.FileField(upload_to="assessments/media/", blank=True, null=True)
    url = models.URLField(blank=True)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["question_id", "order", "id"]

    def __str__(self) -> str:
        return f"{self.question_id}-{self.media_type}"


class HintResource(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="hint_resources")
    title = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.title or self.url or f"Hint {self.id}"


class Submission(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    user_identifier = models.CharField(max_length=64, verbose_name=_("شناسه کاربر/مهمان"))
    full_name = models.CharField(max_length=150, verbose_name=_("نام"), blank=True)
    email = models.EmailField(verbose_name=_("ایمیل"), blank=True)
    score = models.FloatField(default=0)
    total_weight = models.FloatField(default=0)
    ratio = models.FloatField(default=0)
    duration_seconds = models.PositiveIntegerField(default=0)
    recommended_level = models.CharField(max_length=2, choices=Assessment.LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class SubmissionItem(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="items")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice_id = models.IntegerField(null=True, blank=True)
    user_text = models.CharField(max_length=300, blank=True)
    is_correct = models.BooleanField(default=False)
    gained_score = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"Answer to Q{self.question_id}"

