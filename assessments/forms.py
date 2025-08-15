from django import forms
from .models import Assessment, Question


class AssessmentStartForm(forms.Form):
    assessment = forms.ModelChoiceField(queryset=Assessment.objects.filter(is_active=True))


def build_assessment_form(assessment: Assessment, questions=None):
    class _AssessmentForm(forms.Form):
        full_name = forms.CharField(max_length=150, required=False, label="نام")
        email = forms.EmailField(required=False, label="ایمیل")

    qs = questions if questions is not None else assessment.questions.all()
    for question in qs:
        field_name = f"q_{question.id}"
        if question.type == Question.QuestionType.MCQ_SINGLE:
            _AssessmentForm.base_fields[field_name] = forms.ChoiceField(
                label=question.text,
                widget=forms.RadioSelect,
                choices=[(c.id, c.text) for c in question.choices.all()],
            )
        elif question.type == Question.QuestionType.MULTI:
            _AssessmentForm.base_fields[field_name] = forms.MultipleChoiceField(
                label=question.text,
                widget=forms.CheckboxSelectMultiple,
                choices=[(c.id, c.text) for c in question.choices.all()],
                required=False,
            )
        elif question.type == Question.QuestionType.TF:
            _AssessmentForm.base_fields[field_name] = forms.ChoiceField(
                label=question.text,
                widget=forms.RadioSelect,
                choices=[("true", "درست"), ("false", "نادرست")],
            )
        elif question.type == Question.QuestionType.FILL:
            _AssessmentForm.base_fields[field_name] = forms.CharField(
                label=question.text,
                widget=forms.TextInput(attrs={"placeholder": "..."}),
            )
        elif question.type == Question.QuestionType.ORDER:
            help_items = ", ".join([f"{it.id}:{it.text}" for it in question.ordering_items.all()])
            _AssessmentForm.base_fields[field_name] = forms.CharField(
                label=f"{question.text}",
                help_text=f"شناسه‌ها را به‌ترتیب با کاما وارد کنید: {help_items}",
                widget=forms.TextInput(attrs={"placeholder": "مثال: 3,1,2,4"}),
                required=False,
            )
        elif question.type == Question.QuestionType.MATCH:
            lefts = ", ".join([p.left_text for p in question.match_pairs.all()])
            _AssessmentForm.base_fields[field_name] = forms.CharField(
                label=f"{question.text}",
                help_text=f"هر سطر به قالب left=right. گزینه‌های چپ: {lefts}",
                widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Haus=House\nBuch=Book"}),
                required=False,
            )
    return _AssessmentForm


