#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sami.settings')
django.setup()

from blog.models import Category, Post
from django.utils.translation import activate

def create_sample_data():
    print("Creating sample blog data...")
    
    # Create categories
    categories = [
        {
            'name': 'گرامر',
            'slug': 'grammar',
            'description': 'مقالات مربوط به گرامر زبان آلمانی',
            'color': '#007bff'
        },
        {
            'name': 'مکالمه',
            'slug': 'speaking',
            'description': 'مقالات مربوط به مکالمه و گفتگو',
            'color': '#28a745'
        },
        {
            'name': 'واژگان',
            'slug': 'vocabulary',
            'description': 'مقالات مربوط به واژگان و لغات',
            'color': '#ffc107'
        },
        {
            'name': 'فرهنگ',
            'slug': 'culture',
            'description': 'مقالات مربوط به فرهنگ آلمان',
            'color': '#dc3545'
        }
    ]
    
    created_categories = []
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")
        created_categories.append(category)
    
    # Create sample posts
    posts = [
        {
            'title': 'آموزش حروف تعریف در زبان آلمانی',
            'slug': 'german-articles',
            'content': '''حروف تعریف در زبان آلمانی یکی از مهم‌ترین بخش‌های گرامر است. در این مقاله به بررسی انواع حروف تعریف و نحوه استفاده از آنها می‌پردازیم.

حروف تعریف معین (der, die, das):
- der: برای اسامی مذکر
- die: برای اسامی مؤنث  
- das: برای اسامی خنثی

حروف تعریف نامعین (ein, eine, ein):
- ein: برای اسامی مذکر و خنثی
- eine: برای اسامی مؤنث

نکات مهم:
1. حروف تعریف با جنسیت اسم تغییر می‌کنند
2. در حالت جمع، همه اسامی از "die" استفاده می‌کنند
3. حروف تعریف با حالت دستوری (nominativ, akkusativ, dativ, genitiv) تغییر می‌کنند''',
            'excerpt': 'آموزش کامل حروف تعریف در زبان آلمانی با مثال‌های کاربردی',
            'category': created_categories[0],  # گرامر
            'is_featured': True,
            'youtube_video_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'اصول مکالمه روزمره در آلمان',
            'slug': 'daily-conversation-german',
            'content': '''مکالمه روزمره در آلمان شامل عبارات و جملات پرکاربردی است که در زندگی روزانه استفاده می‌شود.

عبارات احوالپرسی:
- Guten Morgen: صبح بخیر
- Guten Tag: روز بخیر
- Guten Abend: عصر بخیر
- Auf Wiedersehen: خداحافظ

عبارات مفید:
- Wie geht es Ihnen?: حال شما چطور است؟
- Danke, gut: ممنون، خوبم
- Bitte: لطفاً / خواهش می‌کنم
- Entschuldigung: عذر می‌خواهم

نکات مهم در مکالمه:
1. استفاده از "Sie" برای افراد محترم
2. استفاده از "du" برای دوستان و خانواده
3. رعایت آداب معاشرت آلمانی
4. تلفظ صحیح کلمات''',
            'excerpt': 'آموزش عبارات و جملات پرکاربرد در مکالمه روزمره آلمانی',
            'category': created_categories[1],  # مکالمه
            'is_featured': False,
            'youtube_video_id': None
        },
        {
            'title': '100 کلمه ضروری برای سفر به آلمان',
            'slug': 'essential-german-words-travel',
            'content': '''در این مقاله، 100 کلمه ضروری برای سفر به آلمان را معرفی می‌کنیم.

کلمات مربوط به سفر:
- Reise: سفر
- Flughafen: فرودگاه
- Bahnhof: ایستگاه قطار
- Hotel: هتل
- Restaurant: رستوران

کلمات مربوط به غذا:
- Brot: نان
- Wasser: آب
- Kaffee: قهوه
- Bier: آبجو
- Wurst: سوسیس

کلمات مربوط به خرید:
- Geld: پول
- Preis: قیمت
- Billig: ارزان
- Teuer: گران
- Rabatt: تخفیف

نکات مهم:
1. یادگیری تلفظ صحیح کلمات
2. استفاده از کلمات در جمله
3. تمرین روزانه
4. استفاده از اپلیکیشن‌های یادگیری''',
            'excerpt': '100 کلمه ضروری و پرکاربرد برای سفر به آلمان',
            'category': created_categories[2],  # واژگان
            'is_featured': True,
            'youtube_video_id': 'jNQXAC9IVRw'
        }
    ]
    
    for post_data in posts:
        # Check if post exists by looking for translations
        existing_post = Post.objects.filter(translations__slug=post_data['slug']).first()
        
        if existing_post:
            print(f"Post already exists: {post_data['title']}")
            continue
        
        # Create new post
        post = Post.objects.create(
            category=post_data['category'],
            is_featured=post_data['is_featured'],
            youtube_video_id=post_data['youtube_video_id']
        )
        
        # Set translated fields
        post.set_current_language('fa')
        post.title = post_data['title']
        post.slug = post_data['slug']
        post.content = post_data['content']
        post.excerpt = post_data['excerpt']
        post.save()
        
        print(f"Created post: {post.title}")
    
    print("\nSample data creation completed!")
    print(f"Created {len(created_categories)} categories and {len(posts)} posts")

if __name__ == '__main__':
    create_sample_data()
