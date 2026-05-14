from django import forms
from django.core.validators import RegexValidator

from .models import Program, Plan, Week, Month, Day, ProgramItem, WorkoutItem, WaterTarget, SiteSettings


COLOR_VALIDATOR = RegexValidator(
    regex=r'^#[0-9A-Fa-f]{6}$',
    message='Enter a valid hex color such as #ff6417.',
)


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

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'goal_type', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Program name'}),
            'goal_type': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the program', 'rows': 4}),
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
        fields = ['program', 'name', 'plan_type', 'count', 'description', 'is_active']
        widgets = {
            'program': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Plan name'}),
            'plan_type': forms.Select(attrs={'class': 'form-input'}),
            'count': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'placeholder': 'Number of periods'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the plan', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }


class WeekForm(forms.ModelForm):
    class Meta:
        model = Week
        fields = ['plan', 'week_number', 'title', 'description', 'is_active']
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-input'}),
            'week_number': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Week title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the week', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }


class MonthForm(forms.ModelForm):
    class Meta:
        model = Month
        fields = ['plan', 'month_number', 'title', 'description', 'is_active']
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-input'}),
            'month_number': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Month title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the month', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['plan', 'day_number', 'title', 'description', 'is_active']
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-input'}),
            'day_number': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Day title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the day', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }


class ProgramItemForm(forms.ModelForm):
    class Meta:
        model = ProgramItem
        fields = ['day', 'title', 'image', 'description', 'meal_category', 'start_time', 'end_time', 'display_order', 'is_active']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Program title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the program', 'rows': 5}),
            'meal_category': forms.Select(attrs={'class': 'form-input'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
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


class WorkoutItemForm(forms.ModelForm):
    class Meta:
        model = WorkoutItem
        fields = ['day', 'title', 'image', 'description', 'duration', 'display_order', 'is_active']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Workout title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe the workout', 'rows': 5}),
            'duration': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 30 minutes'}),
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


class WaterTargetForm(forms.ModelForm):
    class Meta:
        model = WaterTarget
        fields = ['day', 'target_amount', 'reminder_note', 'display_order', 'is_active']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-input'}),
            'target_amount': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 2 liters'}),
            'reminder_note': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Reminder note for water intake', 'rows': 4}),
            'display_order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-input'}),
        }

    def clean_target_amount(self):
        target_amount = self.cleaned_data.get('target_amount', '').strip()
        if not target_amount:
            raise forms.ValidationError('Please enter a target water amount.')
        return target_amount
