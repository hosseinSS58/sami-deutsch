# راهنمای استخراج و وارد کردن داده‌های Assessments

این راهنما نحوه استخراج داده‌های بخش Assessments از یک دیتابیس و وارد کردن آن‌ها به دیتابیس دیگری را توضیح می‌دهد.

## مراحل استخراج (Export)

### 1. استخراج داده‌های اصلی (بدون Submission ها)

```bash
python manage.py export_assessments
```

این دستور یک فایل JSON با نام `assessments_export.json` در همان پوشه ایجاد می‌کند که شامل:
- Assessment ها
- Question ها
- Choice ها
- AnswerPattern ها
- OrderingItem ها
- MatchPair ها
- QuestionMedia ها (اطلاعات فایل‌ها)

### 2. استخراج با شامل کردن Submission ها

اگر می‌خواهید نتیجه آزمون‌های کاربران را هم استخراج کنید:

```bash
python manage.py export_assessments --include-submissions
```

### 3. استخراج همراه با کپی فایل‌های رسانه‌ای

اگر سوالات شما دارای عکس، فیلم یا صوت هستند و می‌خواهید فایل‌های آن‌ها را هم کپی کنید:

```bash
python manage.py export_assessments --include-media-files
```

یا برای مشخص کردن مسیر پوشه مقصد:

```bash
python manage.py export_assessments --include-media-files --media-dir my_media_files
```

### 4. استخراج کامل (همه چیز)

```bash
python manage.py export_assessments --include-submissions --include-media-files
```

### 5. تعیین نام فایل خروجی

```bash
python manage.py export_assessments --output my_assessments.json
```

## مراحل وارد کردن (Import)

### 1. وارد کردن داده‌های اصلی

```bash
python manage.py import_assessments assessments_export.json
```

### 2. پاک کردن داده‌های قبلی قبل از وارد کردن

⚠️ **هشدار**: این گزینه تمام داده‌های Assessment موجود را پاک می‌کند!

```bash
python manage.py import_assessments assessments_export.json --clear-existing
```

### 3. وارد کردن فایل‌های رسانه‌ای

اگر فایل‌های رسانه‌ای را در یک پوشه دارید:

```bash
python manage.py import_assessments assessments_export.json --media-dir assessments_export_media
```

### 4. رد کردن Submission ها

اگر فایل JSON شامل Submission ها باشد اما شما نمی‌خواهید آن‌ها را وارد کنید:

```bash
python manage.py import_assessments assessments_export.json --skip-submissions
```

## مثال کامل: انتقال از سرور A به سرور B

### در سرور A (سرور فعلی):

```bash
# 1. استخراج داده‌ها با فایل‌های رسانه‌ای
python manage.py export_assessments --include-media-files --output assessments_data.json

# 2. دانلود فایل JSON و پوشه media از سرور
# (مثلا با scp, FTP, یا FileZilla)
```

### در سرور B (هاست جدید):

```bash
# 1. آپلود فایل JSON و پوشه media به سرور جدید

# 2. وارد کردن داده‌ها
python manage.py import_assessments assessments_data.json --media-dir assessments_export_media

# یا اگر می‌خواهید داده‌های قبلی را پاک کنید:
python manage.py import_assessments assessments_data.json --clear-existing --media-dir assessments_export_media
```

## ساختار فایل JSON

فایل JSON خروجی شامل بخش‌های زیر است:

```json
{
  "assessments": [...],          // لیست Assessment ها
  "questions": [...],            // لیست Question ها
  "choices": [...],              // لیست Choice ها
  "answer_patterns": [...],      // لیست AnswerPattern ها
  "ordering_items": [...],       // لیست OrderingItem ها
  "match_pairs": [...],          // لیست MatchPair ها
  "question_media": [...],       // لیست QuestionMedia ها
  "submissions": [...],          // (اختیاری) لیست Submission ها
  "submission_items": [...],     // (اختیاری) لیست SubmissionItem ها
  "id_mapping": {...}            // نگاشت ID های قدیمی به جدید
}
```

## نکات مهم

1. **فایل‌های رسانه‌ای**: اگر فایل‌های رسانه‌ای را کپی کرده‌اید، باید آن‌ها را به پوشه `media/assessments/media/` در سرور جدید آپلود کنید یا از گزینه `--media-dir` استفاده کنید.

2. **ID ها**: ID های جدید به صورت خودکار تولید می‌شوند. روابط بین جداول حفظ می‌شود.

3. **User ID در Submission ها**: اگر Submission ها را وارد می‌کنید، User ID ها ممکن است در دیتابیس جدید موجود نباشند. در این صورت `user_id` به صورت NULL ذخیره می‌شود.

4. **پشتیبان‌گیری**: قبل از استفاده از `--clear-existing` حتماً از دیتابیس فعلی پشتیبان‌گیری کنید!

## مشکلات احتمالی و راه حل

### خطا در وارد کردن فایل‌های رسانه‌ای

اگر فایل‌های رسانه‌ای به درستی وارد نشدند:
- مطمئن شوید پوشه media وجود دارد
- نام فایل‌ها باید به صورت `{export_id}_{filename}` باشد
- یا می‌توانید فایل‌ها را به صورت دستی به `media/assessments/media/` آپلود کنید

### خطای مربوط به Foreign Key

اگر خطای Foreign Key دریافت کردید:
- مطمئن شوید که تمام Assessment ها قبل از Question ها وارد شده‌اند
- از گزینه `--clear-existing` استفاده کنید

### خطای Encoding

اگر مشکل Encoding داشتید، مطمئن شوید که از UTF-8 استفاده می‌کنید.



