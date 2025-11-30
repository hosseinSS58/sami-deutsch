from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Profile


User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label=_("ایمیل"), required=True)
    first_name = forms.CharField(label=_("نام"), required=False)
    last_name = forms.CharField(label=_("نام خانوادگی"), required=False)

    newsletter_opt_in = forms.BooleanField(label=_("عضویت در خبرنامه"), required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "newsletter_opt_in",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("این ایمیل قبلاً ثبت شده است"))
        return email

    def save(self, commit=True):
        user = super().save(commit)
        # Persist profile data
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.newsletter_opt_in = bool(self.cleaned_data.get("newsletter_opt_in"))
        if commit:
            profile.save()
        return user


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(label=_("نام کاربری یا ایمیل"))

    def clean(self):
        # Allow login via email
        username = self.cleaned_data.get("username", "")
        if "@" in username and not User.objects.filter(email__iexact=username).exists():
            # Let base class raise the proper error
            return super().clean()
        if "@" in username:
            try:
                user = User.objects.get(email__iexact=username)
                self.cleaned_data["username"] = user.get_username()
            except User.DoesNotExist:
                pass
        return super().clean()


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile with file upload validation"""
    
    class Meta:
        model = Profile
        fields = ["avatar", "phone", "level", "bio", "website", "newsletter_opt_in"]
        widgets = {
            "avatar": forms.FileInput(attrs={"accept": "image/jpeg,image/png,image/webp"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            # Check file size (2MB limit)
            max_size = 2 * 1024 * 1024  # 2MB
            if avatar.size > max_size:
                raise forms.ValidationError(
                    _("اندازه فایل باید کمتر از 2 مگابایت باشد.")
                )
            
            # Check file type
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
            if avatar.content_type not in allowed_types:
                raise forms.ValidationError(
                    _("فقط فایل‌های تصویری با فرمت JPEG, PNG یا WebP مجاز هستند.")
                )
            
            # Additional check: verify it's actually an image
            from PIL import Image
            try:
                img = Image.open(avatar)
                img.verify()
            except Exception:
                raise forms.ValidationError(
                    _("فایل انتخاب شده یک تصویر معتبر نیست.")
                )
        
        return avatar
    
    def clean_website(self):
        website = self.cleaned_data.get("website", "").strip()
        if website:
            # Ensure URL starts with http:// or https://
            if not website.startswith(("http://", "https://")):
                website = "https://" + website
        return website




