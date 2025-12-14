from django.contrib import admin
from .models import (
    Assessment,
    Question,
    Choice,
    Submission,
    AnswerPattern,
    SubmissionItem,
    OrderingItem,
    MatchPair,
    QuestionMedia,
    HintResource,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class QuestionMediaInline(admin.TabularInline):
    model = QuestionMedia
    extra = 1


class HintResourceInline(admin.TabularInline):
    model = HintResource
    extra = 1


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "is_active", "created_at")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("assessment", "text", "type", "difficulty", "weight")
    inlines = [ChoiceInline, QuestionMediaInline, HintResourceInline]


@admin.register(OrderingItem)
class OrderingItemAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "correct_position")


@admin.register(MatchPair)
class MatchPairAdmin(admin.ModelAdmin):
    list_display = ("question", "left_text", "right_text")


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "is_correct")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("assessment", "user_identifier", "score", "recommended_level", "created_at")


@admin.register(AnswerPattern)
class AnswerPatternAdmin(admin.ModelAdmin):
    list_display = ("question", "kind", "pattern")


@admin.register(SubmissionItem)
class SubmissionItemAdmin(admin.ModelAdmin):
    list_display = ("submission", "question", "is_correct", "gained_score")

# Register your models here.
