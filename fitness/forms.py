from django import forms
from django.core.validators import RegexValidator

from .models import Program, Plan, Week, Month, Day, ProgramItem, WorkoutItem, DayMedia, WaterTarget, SiteSettings


COLOR_VALIDATOR = RegexValidator(
    regex=r'^#[0-9A-Fa-f]{6}$',
    message='Enter a valid hex color such as #ff6417.',
)

ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
ALLOWED_VIDEO_TYPES = {'video/mp4', 'video/webm', 'video/quicktime', 'video/x-m4v'}


def validate_media_upload(upload, allowed_types, label):
    """Validate media type before storage sends the file to Cloudinary."""
    if not upload:
        return upload
    content_type = getattr(upload, 'content_type', '')
    if content_type and content_type not in allowed_types:
        raise forms.ValidationError(f'Unsupported {label} type.')
    return upload


class BaseSettingsForm(forms.ModelForm):
    def _apply_widget_classes(self):
        for field in self.fields.values():
            css_class = 'form-input'
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing} {css_class}'.strip()


class SiteSettingsForm(BaseSettingsForm):
    class Meta:
        model = SiteSettings
        fields = [
            'default_workout_duration',
            'meal_timing_preference',
            'water_reminder_interval',
            'publishing_mode',
            'enable_weight_loss_programs',
            'enable_weight_gain_programs',
            'auto_publish_programs',
            'default_language',
            'timezone',
            'date_format',
            'measurement_unit',
            'currency',
            'region',
            'support_email',
            'support_phone',
            'support_working_hours',
            'help_center_url',
            'enable_live_chat',
            'enable_email_notifications',
            'enable_push_notifications',
            'enable_water_reminders',
            'enable_admin_alerts',
        ]
        widgets = {
            'support_working_hours': forms.TextInput(attrs={'placeholder': 'Mon-Sat, 9:00 AM - 6:00 PM'}),
            'help_center_url': forms.URLInput(attrs={'placeholder': 'https://help.scalefit.com'}),
            'region': forms.TextInput(attrs={'placeholder': 'India'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_workout_duration = self.instance.default_workout_duration if self.instance.pk else None
        self._apply_widget_classes()

    def save(self, commit=True):
        settings = super().save(commit=commit)

        if (
            commit
            and 'default_workout_duration' in self.changed_data
            and self._original_workout_duration != settings.default_workout_duration
        ):
            WorkoutItem.objects.update(duration=settings.workout_duration_label)

        return settings


class SiteAppearanceSettingsForm(BaseSettingsForm):
    primary_theme_color = forms.CharField(validators=[COLOR_VALIDATOR], widget=forms.TextInput(attrs={'type': 'color'}))
    secondary_theme_color = forms.CharField(validators=[COLOR_VALIDATOR], widget=forms.TextInput(attrs={'type': 'color'}))

    class Meta:
        model = SiteSettings
        fields = [
            'primary_theme_color',
            'secondary_theme_color',
            'enable_dark_mode',
            'site_logo',
            'favicon',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_widget_classes()

    def clean_site_logo(self):
        return validate_media_upload(self.cleaned_data.get('site_logo'), ALLOWED_IMAGE_TYPES, 'site logo')

    def clean_favicon(self):
        return validate_media_upload(self.cleaned_data.get('favicon'), ALLOWED_IMAGE_TYPES, 'favicon')

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'name_ta', 'name_hi', 'goal_type', 'description', 'description_ta', 'description_hi', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Program name'}),
            'name_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Program name in Tamil'}),
            'name_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Program name in Hindi'}),
            'goal_type': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the program', 'rows': 4}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the program in Tamil', 'rows': 4}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the program in Hindi', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = SiteSettings.get_solo()
        if not self.instance.pk:
            self.initial['is_active'] = settings.should_auto_publish


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['program', 'name', 'name_ta', 'name_hi', 'plan_type', 'count', 'description', 'description_ta', 'description_hi', 'is_active']
        widgets = {
            'program': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Plan name'}),
            'name_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Plan name in Tamil'}),
            'name_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Plan name in Hindi'}),
            'plan_type': forms.Select(attrs={'class': 'form-input'}),
            'count': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'placeholder': 'Number of periods'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the plan', 'rows': 4}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the plan in Tamil', 'rows': 4}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the plan in Hindi', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }


class WeekForm(forms.ModelForm):
    class Meta:
        model = Week
        fields = ['plan', 'week_number', 'title', 'title_ta', 'title_hi', 'description', 'description_ta', 'description_hi', 'is_active']
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-input'}),
            'week_number': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Week title'}),
            'title_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Week title in Tamil'}),
            'title_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Week title in Hindi'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the week', 'rows': 4}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the week in Tamil', 'rows': 4}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the week in Hindi', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }


class MonthForm(forms.ModelForm):
    class Meta:
        model = Month
        fields = ['plan', 'month_number', 'title', 'title_ta', 'title_hi', 'description', 'description_ta', 'description_hi', 'is_active']
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-input'}),
            'month_number': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Month title'}),
            'title_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Month title in Tamil'}),
            'title_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Month title in Hindi'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the month', 'rows': 4}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the month in Tamil', 'rows': 4}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the month in Hindi', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['plan', 'day_number', 'title', 'title_ta', 'title_hi', 'description', 'description_ta', 'description_hi', 'is_active']
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-input'}),
            'day_number': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Day title'}),
            'title_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Day title in Tamil'}),
            'title_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Day title in Hindi'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the day', 'rows': 4}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the day in Tamil', 'rows': 4}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the day in Hindi', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }


class ProgramItemForm(forms.ModelForm):
    class Meta:
        model = ProgramItem
        fields = [
            'day', 'title', 'title_ta', 'title_hi', 'image', 'video', 'description', 'description_ta', 'description_hi', 'meal_category', 'start_time', 'end_time',
            'calories', 'protein', 'carbs', 'fat', 'fiber', 'vitamins', 'minerals',
            'hydration', 'hydration_ta', 'hydration_hi', 'benefits', 'benefits_ta', 'benefits_hi',
            'diet_type', 'sugar', 'sodium', 'cholesterol',
            'display_order', 'is_active'
        ]
        widgets = {
            'day': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Program title'}),
            'title_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Program title in Tamil'}),
            'title_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Program title in Hindi'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the program', 'rows': 5}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the program in Tamil', 'rows': 5}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the program in Hindi', 'rows': 5}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'video/mp4,video/webm,video/quicktime'}),
            'meal_category': forms.Select(attrs={'class': 'form-input'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
            'calories': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'protein': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': 0}),
            'carbs': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': 0}),
            'fat': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': 0}),
            'fiber': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': 0}),
            'vitamins': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Vitamin A, Vitamin C'}),
            'minerals': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Iron, Calcium'}),
            'hydration': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Drink 500ml water'}),
            'hydration_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Hydration tip in Tamil'}),
            'hydration_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Hydration tip in Hindi'}),
            'benefits': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., High protein, Muscle recovery'}),
            'benefits_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Benefits in Tamil'}),
            'benefits_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Benefits in Hindi'}),
            'diet_type': forms.Select(attrs={'class': 'form-input'}),
            'sugar': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': 0}),
            'sodium': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': 0}),
            'cholesterol': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_sections = SiteSettings.get_solo().meal_sections
        choices = [
            (value, label)
            for value, label in ProgramItem.CATEGORY_CHOICES
            if value in active_sections
        ]
        self.fields['meal_category'].choices = choices

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Please enter a title for the program item.')
        return title

    def clean_image(self):
        return validate_media_upload(self.cleaned_data.get('image'), ALLOWED_IMAGE_TYPES, 'image')

    def clean_video(self):
        return validate_media_upload(self.cleaned_data.get('video'), ALLOWED_VIDEO_TYPES, 'video')


class WorkoutItemForm(forms.ModelForm):
    class Meta:
        model = WorkoutItem
        fields = ['day', 'title', 'title_ta', 'title_hi', 'image', 'video', 'description', 'description_ta', 'description_hi', 'duration', 'display_order', 'is_active']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Workout title'}),
            'title_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Workout title in Tamil'}),
            'title_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Workout title in Hindi'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the workout', 'rows': 5}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the workout in Tamil', 'rows': 5}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the workout in Hindi', 'rows': 5}),
            'duration': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 30 minutes'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'video/mp4,video/webm,video/quicktime'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['duration'].initial = SiteSettings.get_solo().workout_duration_label

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Please enter a title for the workout.')
        return title

    def clean_image(self):
        return validate_media_upload(self.cleaned_data.get('image'), ALLOWED_IMAGE_TYPES, 'image')

    def clean_video(self):
        return validate_media_upload(self.cleaned_data.get('video'), ALLOWED_VIDEO_TYPES, 'video')


class DayMediaForm(forms.ModelForm):
    class Meta:
        model = DayMedia
        fields = [
            'media_type', 'media_file', 'title', 'title_ta', 'title_hi',
            'description', 'description_ta', 'description_hi', 'display_order', 'is_active'
        ]
        widgets = {
            'media_type': forms.Select(attrs={'class': 'form-input'}),
            'media_file': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'image/jpeg,image/png,image/webp,image/gif,video/mp4,video/webm,video/quicktime'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Media title'}),
            'title_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Media title in Tamil'}),
            'title_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Media title in Hindi'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Instructions or description for this media', 'rows': 5}),
            'description_ta': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Instructions in Tamil', 'rows': 5}),
            'description_hi': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Instructions in Hindi', 'rows': 5}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Please enter a title for this media.')
        return title

    def clean_media_file(self):
        upload = self.cleaned_data.get('media_file')
        media_type = self.cleaned_data.get('media_type')
        if not upload:
            return upload
        if media_type == DayMedia.WORKOUT_VIDEO:
            return validate_media_upload(upload, ALLOWED_VIDEO_TYPES, 'video')
        return validate_media_upload(upload, ALLOWED_IMAGE_TYPES, 'image/GIF')


class WaterTargetForm(forms.ModelForm):
    class Meta:
        model = WaterTarget
        fields = ['day', 'target_amount', 'target_amount_ta', 'target_amount_hi', 'reminder_note', 'reminder_note_ta', 'reminder_note_hi', 'display_order', 'is_active']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-input'}),
            'target_amount': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 2 liters'}),
            'target_amount_ta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Target amount in Tamil'}),
            'target_amount_hi': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Target amount in Hindi'}),
            'reminder_note': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Reminder note for water intake', 'rows': 4}),
            'reminder_note_ta': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Reminder note in Tamil', 'rows': 4}),
            'reminder_note_hi': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Reminder note in Hindi', 'rows': 4}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }

    def clean_target_amount(self):
        target_amount = self.cleaned_data.get('target_amount', '').strip()
        if not target_amount:
            raise forms.ValidationError('Please enter a target water amount.')
        return target_amount
