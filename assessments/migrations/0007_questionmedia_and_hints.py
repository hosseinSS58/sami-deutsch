from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("assessments", "0006_alter_question_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="hint_links",
            field=models.JSONField(blank=True, default=list, verbose_name="لینک‌های پیشنهادی پس از پاسخ نادرست"),
        ),
        migrations.AddField(
            model_name="question",
            name="hint_text",
            field=models.TextField(blank=True, verbose_name="نکته/توضیح پس از پاسخ نادرست"),
        ),
        migrations.CreateModel(
            name="QuestionMedia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("media_type", models.CharField(choices=[("image", "تصویر"), ("audio", "صوت"), ("video", "ویدیو"), ("text", "متن"), ("file", "فایل")], default="image", max_length=10)),
                ("file", models.FileField(blank=True, null=True, upload_to="assessments/media/")),
                ("url", models.URLField(blank=True)),
                ("caption", models.CharField(blank=True, max_length=200)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="media_items", to="assessments.question")),
            ],
            options={
                "ordering": ["question_id", "order", "id"],
            },
        ),
        migrations.CreateModel(
            name="HintResource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=200)),
                ("url", models.URLField(blank=True)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="hint_resources", to="assessments.question")),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
    ]


