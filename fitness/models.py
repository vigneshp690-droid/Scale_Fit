import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import get_language, gettext_lazy as _

from .media_storage import cloudinary_upload_path

try:
    from cloudinary.models import CloudinaryField
except ImportError:
    CloudinaryField = None


def cloudinary_or_file_field(resource_type, folder, fallback_field=models.FileField, **kwargs):
    if CloudinaryField:
        return CloudinaryField(resource_type=resource_type, folder=f'cloudinary/{folder}', **kwargs)
    return fallback_field(upload_to=cloudinary_upload_path(folder), **kwargs)


def get_localized_field_value(instance, field_name):
    from django.utils.translation import gettext
    language_code = (get_language() or 'en').split('-')[0]
    if language_code in {'ta', 'hi'}:
        translated_value = getattr(instance, f'{field_name}_{language_code}', '')
        if translated_value:
            return translated_value
    
    original_value = getattr(instance, field_name, '')
    if original_value and language_code != 'en':
        return gettext(original_value)
    return original_value


class SiteSettings(models.Model):
    DURATION_30 = 30
    DURATION_45 = 45
    DURATION_60 = 60
    DURATION_90 = 90
    WORKOUT_DURATION_CHOICES = [
        (DURATION_30, '30 mins'),
        (DURATION_45, '45 mins'),
        (DURATION_60, '60 mins'),
        (DURATION_90, '90 mins'),
    ]

    MEAL_THREE = 'three_meals'
    MEAL_FOUR = 'four_meals'
    MEAL_FIVE = 'five_meals'
    MEAL_TIMING_CHOICES = [
        (MEAL_THREE, 'Breakfast, Lunch, Dinner'),
        (MEAL_FOUR, 'Breakfast, Lunch, Snack, Dinner'),
        (MEAL_FIVE, '5 Meals Plan'),
    ]
    MEAL_SECTIONS = {
        MEAL_THREE: ['breakfast', 'lunch', 'dinner'],
        MEAL_FOUR: ['breakfast', 'lunch', 'snacks', 'dinner'],
        MEAL_FIVE: ['breakfast', 'snacks', 'lunch', 'snacks', 'dinner'],
    }

    WATER_30 = 30
    WATER_60 = 60
    WATER_90 = 90
    WATER_120 = 120
    WATER_INTERVAL_CHOICES = [
        (WATER_30, '30 mins'),
        (WATER_60, '60 mins'),
        (WATER_90, '90 mins'),
        (WATER_120, '120 mins'),
    ]

    PUBLISH_AUTO = 'auto'
    PUBLISH_REVIEW = 'review'
    PUBLISHING_MODE_CHOICES = [
        (PUBLISH_AUTO, 'Auto Publish'),
        (PUBLISH_REVIEW, 'Review Before Publish'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ta', 'Tamil'),
        ('hi', 'Hindi'),
    ]
    TIMEZONE_CHOICES = [
        ('Asia/Kolkata', 'Asia/Kolkata'),
        ('UTC', 'UTC'),
        ('America/New_York', 'America/New_York'),
    ]
    DATE_FORMAT_CHOICES = [
        ('d/m/Y', 'DD/MM/YYYY'),
        ('m/d/Y', 'MM/DD/YYYY'),
        ('Y-m-d', 'YYYY-MM-DD'),
    ]
    MEASUREMENT_CHOICES = [
        ('kg', 'KG'),
        ('lb', 'LB'),
    ]
    CURRENCY_CHOICES = [
        ('INR', 'INR'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
    ]

    singleton_key = models.PositiveSmallIntegerField(default=1, unique=True, editable=False)

    default_workout_duration = models.PositiveSmallIntegerField(choices=WORKOUT_DURATION_CHOICES, default=DURATION_45)
    meal_timing_preference = models.CharField(max_length=24, choices=MEAL_TIMING_CHOICES, default=MEAL_FOUR)
    water_reminder_interval = models.PositiveSmallIntegerField(choices=WATER_INTERVAL_CHOICES, default=WATER_60)
    publishing_mode = models.CharField(max_length=12, choices=PUBLISHING_MODE_CHOICES, default=PUBLISH_REVIEW)
    enable_weight_loss_programs = models.BooleanField(default=True)
    enable_weight_gain_programs = models.BooleanField(default=True)
    auto_publish_programs = models.BooleanField(default=False)

    default_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='en')
    timezone = models.CharField(max_length=64, choices=TIMEZONE_CHOICES, default='Asia/Kolkata')
    date_format = models.CharField(max_length=16, choices=DATE_FORMAT_CHOICES, default='d/m/Y')
    measurement_unit = models.CharField(max_length=8, choices=MEASUREMENT_CHOICES, default='kg')
    currency = models.CharField(max_length=8, choices=CURRENCY_CHOICES, default='INR')
    region = models.CharField(max_length=80, default='India')

    support_email = models.EmailField(default='support@scalefit.com')
    support_phone = models.CharField(max_length=32, blank=True, default='')
    support_working_hours = models.CharField(max_length=120, default='Mon-Sat, 9:00 AM - 6:00 PM')
    help_center_url = models.URLField(blank=True, default='')
    enable_live_chat = models.BooleanField(default=False)

    enable_email_notifications = models.BooleanField(default=True)
    enable_push_notifications = models.BooleanField(default=False)
    enable_water_reminders = models.BooleanField(default=True)
    enable_admin_alerts = models.BooleanField(default=True)

    primary_theme_color = models.CharField(max_length=7, default='#ff6417')
    secondary_theme_color = models.CharField(max_length=7, default='#19b8c9')
    enable_dark_mode = models.BooleanField(default=False)
    # Site branding uploads to Cloudinary when configured. The database stores
    # only the media path/URL, not binary image data.
    site_logo = models.ImageField(upload_to=cloudinary_upload_path('site_settings'), blank=True, null=True)
    favicon = models.ImageField(upload_to=cloudinary_upload_path('site_settings'), blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'ScaleFit Site Settings'

    def save(self, *args, **kwargs):
        self.singleton_key = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        settings = cls.objects.first()
        if settings:
            return settings
        return cls.objects.create()

    @property
    def meal_sections(self):
        return self.MEAL_SECTIONS.get(self.meal_timing_preference, self.MEAL_SECTIONS[self.MEAL_FOUR])

    @property
    def workout_duration_label(self):
        return f'{self.default_workout_duration} mins'

    @property
    def water_reminder_label(self):
        return f'{self.water_reminder_interval} mins'

    @property
    def should_auto_publish(self):
        return self.auto_publish_programs or self.publishing_mode == self.PUBLISH_AUTO

    def is_goal_enabled(self, goal_type):
        if goal_type == Program.WEIGHT_LOSS:
            return self.enable_weight_loss_programs
        if goal_type == Program.WEIGHT_GAIN:
            return self.enable_weight_gain_programs
        return False

    def enabled_goal_types(self):
        goals = []
        if self.enable_weight_loss_programs:
            goals.append(Program.WEIGHT_LOSS)
        if self.enable_weight_gain_programs:
            goals.append(Program.WEIGHT_GAIN)
        return goals


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Profile and trainer images use Cloudinary-backed storage for scalable
    # uploads while legacy local profile paths remain readable.
    profile_image = models.ImageField(upload_to=cloudinary_upload_path('profile_images'), blank=True, null=True)
    trainer_image = cloudinary_or_file_field(
        'image',
        'trainer_images',
        fallback_field=models.ImageField,
        blank=True,
        null=True,
    )
    mobile_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Mobile number must be exactly 10 digits',
                code='invalid_mobile'
            )
        ],
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.mobile_number}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral_code')
    code = models.CharField(max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    class Meta:
        verbose_name = 'Referral Code'
        verbose_name_plural = 'Referral Codes'


class ReferralSignup(models.Model):
    referral_code = models.ForeignKey(ReferralCode, on_delete=models.CASCADE, related_name='signups')
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referred_by')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referred_user.username} via {self.referral_code.code}"

    class Meta:
        verbose_name = 'Referral Signup'
        verbose_name_plural = 'Referral Signups'


class SiteTheme(models.Model):
    selected_theme = models.CharField(max_length=40, default='scale-orange')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Theme'
        verbose_name_plural = 'Site Theme'

    def __str__(self):
        return self.selected_theme

    @classmethod
    def get_active_slug(cls):
        theme, _ = cls.objects.get_or_create(pk=1)
        return theme.selected_theme

    @classmethod
    def set_active_slug(cls, slug):
        theme, _ = cls.objects.get_or_create(pk=1)
        theme.selected_theme = slug
        theme.save(update_fields=['selected_theme', 'updated_at'])
        return theme


class Program(models.Model):
    WEIGHT_LOSS = 'weight_loss'
    WEIGHT_GAIN = 'weight_gain'
    GOAL_CHOICES = [
        (WEIGHT_LOSS, 'Weight Loss'),
        (WEIGHT_GAIN, 'Weight Gain'),
    ]

    name = models.CharField(max_length=100)
    name_ta = models.CharField(max_length=100, blank=True)
    name_hi = models.CharField(max_length=100, blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_CHOICES)
    description = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'

    def __str__(self):
        return f"{self.name} ({self.get_goal_type_display()})"

    @property
    def translated_name(self):
        return get_localized_field_value(self, 'name')

    @property
    def translated_description(self):
        return get_localized_field_value(self, 'description')

    def save(self, *args, **kwargs):
        settings = SiteSettings.get_solo()
        if settings.should_auto_publish:
            self.is_active = True
        super().save(*args, **kwargs)


class Plan(models.Model):
    PLAN_DAY = 'day'
    PLAN_WEEKLY = 'weekly'
    PLAN_MONTHLY = 'monthly'
    PLAN_TYPE_CHOICES = [
        (PLAN_DAY, 'Day Plan'),
        (PLAN_WEEKLY, 'Weekly Plan'),
        (PLAN_MONTHLY, 'Monthly Plan'),
    ]

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=100)
    name_ta = models.CharField(max_length=100, blank=True)
    name_hi = models.CharField(max_length=100, blank=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES, default=PLAN_DAY)
    count = models.PositiveIntegerField(default=1, help_text='Number of days/weeks/months')
    display_order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['program', 'display_order', 'name']
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'

    def __str__(self):
        return f"{self.program.name} - {self.name} ({self.get_plan_type_display()})"

    @property
    def translated_name(self):
        return get_localized_field_value(self, 'name')

    @property
    def translated_description(self):
        return get_localized_field_value(self, 'description')

    def get_period_count(self):
        """Get count based on plan type"""
        if self.plan_type == self.PLAN_WEEKLY:
            return self.count  # Number of weeks
        elif self.plan_type == self.PLAN_MONTHLY:
            return self.count  # Number of months
        else:  # PLAN_DAY
            return self.count  # Number of days

    def get_period_label(self):
        """Get the label for the period"""
        if self.plan_type == self.PLAN_WEEKLY:
            return "Week"
        elif self.plan_type == self.PLAN_MONTHLY:
            return "Month"
        else:
            return "Day"

    def get_days_count(self):
        """Total days in this plan"""
        if self.plan_type == self.PLAN_WEEKLY:
            return self.count * 7
        elif self.plan_type == self.PLAN_MONTHLY:
            return self.count * 30
        return self.count

    def get_duration_display(self):
        """Human-readable duration label"""
        if self.plan_type == self.PLAN_WEEKLY:
            return f"{self.count} Week{'s' if self.count > 1 else ''}"
        elif self.plan_type == self.PLAN_MONTHLY:
            return f"{self.count} Month{'s' if self.count > 1 else ''}"
        return f"{self.count} Day{'s' if self.count > 1 else ''}"


class Week(models.Model):
    """Groups days into weeks for weekly and monthly plans"""
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='weeks')
    week_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200, blank=True)
    title_ta = models.CharField(max_length=200, blank=True)
    title_hi = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['plan', 'week_number']
        unique_together = ['plan', 'week_number']
        verbose_name = 'Week'
        verbose_name_plural = 'Weeks'

    def __str__(self):
        return f"Week {self.week_number} - {self.plan.name}"

    @property
    def translated_title(self):
        language_code = (get_language() or 'en').split('-')[0]
        if language_code in {'ta', 'hi'}:
            translated_value = getattr(self, f'title_{language_code}', '')
            if translated_value:
                return translated_value
            if self.title == f"Week {self.week_number}":
                if language_code == 'ta':
                    return f"வாரம் {self.week_number}"
                elif language_code == 'hi':
                    return f"सप्ताह {self.week_number}"
        return getattr(self, 'title', '')

    @property
    def translated_description(self):
        return get_localized_field_value(self, 'description')

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Week {self.week_number}"
        super().save(*args, **kwargs)


class Month(models.Model):
    """Groups weeks into months for monthly plans"""
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='months')
    month_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200, blank=True)
    title_ta = models.CharField(max_length=200, blank=True)
    title_hi = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['plan', 'month_number']
        unique_together = ['plan', 'month_number']
        verbose_name = 'Month'
        verbose_name_plural = 'Months'

    def __str__(self):
        return f"Month {self.month_number} - {self.plan.name}"

    @property
    def translated_title(self):
        language_code = (get_language() or 'en').split('-')[0]
        if language_code in {'ta', 'hi'}:
            translated_value = getattr(self, f'title_{language_code}', '')
            if translated_value:
                return translated_value
            if self.title == f"Month {self.month_number}":
                if language_code == 'ta':
                    return f"மாதம் {self.month_number}"
                elif language_code == 'hi':
                    return f"महीना {self.month_number}"
        return getattr(self, 'title', '')

    @property
    def translated_description(self):
        return get_localized_field_value(self, 'description')

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Month {self.month_number}"
        super().save(*args, **kwargs)


class Day(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='days')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='days', null=True, blank=True)
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200, blank=True)
    title_ta = models.CharField(max_length=200, blank=True)
    title_hi = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['plan', 'week', 'day_number']
        verbose_name = 'Day'
        verbose_name_plural = 'Days'

    def __str__(self):
        if self.week:
            return f"Day {self.day_number} - {self.week.title}"
        return f"Day {self.day_number} - {self.plan.name}"

    @property
    def translated_title(self):
        language_code = (get_language() or 'en').split('-')[0]
        if language_code in {'ta', 'hi'}:
            translated_value = getattr(self, f'title_{language_code}', '')
            if translated_value:
                return translated_value
            if self.title == f"Day {self.day_number}":
                if language_code == 'ta':
                    return f"நாள் {self.day_number}"
                elif language_code == 'hi':
                    return f"दिन {self.day_number}"
        return getattr(self, 'title', '')

    @property
    def translated_description(self):
        return get_localized_field_value(self, 'description')

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Day {self.day_number}"
        super().save(*args, **kwargs)


class ProgramItem(models.Model):
    WEIGHT_LOSS = 'weight_loss'
    WEIGHT_GAIN = 'weight_gain'
    GOAL_CHOICES = [
        (WEIGHT_LOSS, 'Weight Loss'),
        (WEIGHT_GAIN, 'Weight Gain'),
    ]

    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
    SNACKS = 'snacks'
    CATEGORY_CHOICES = [
        (BREAKFAST, _('Breakfast')),
        (LUNCH, _('Lunch')),
        (DINNER, _('Dinner')),
        (SNACKS, _('Snacks')),
    ]
    DIET_VEGETARIAN = 'vegetarian'
    DIET_NON_VEGETARIAN = 'non_vegetarian'
    DIET_VEGAN = 'vegan'
    DIET_TYPE_CHOICES = [
        (DIET_VEGETARIAN, _('Vegetarian')),
        (DIET_NON_VEGETARIAN, _('Non-vegetarian')),
        (DIET_VEGAN, _('Vegan')),
    ]

    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='program_items', null=True, blank=True)
    title = models.CharField(max_length=200)
    title_ta = models.CharField(max_length=200, blank=True)
    title_hi = models.CharField(max_length=200, blank=True)
    # Meal media supports images/GIFs plus optional Cloudinary-hosted videos.
    image = models.ImageField(upload_to=cloudinary_upload_path('program_images'), blank=True, null=True)
    video = cloudinary_or_file_field('video', 'program_videos', blank=True, null=True)
    description = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_CHOICES)
    meal_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    # Nutritional Information (Universal Standard)
    calories = models.PositiveIntegerField(blank=True, null=True, help_text="Total calories (kcal)")
    protein = models.FloatField(blank=True, null=True, help_text="Protein in grams")
    carbs = models.FloatField(blank=True, null=True, help_text="Carbohydrates in grams")
    fat = models.FloatField(blank=True, null=True, help_text="Fat in grams")
    fiber = models.FloatField(blank=True, null=True, help_text="Fiber in grams")
    vitamins = models.CharField(max_length=255, blank=True, help_text="e.g., Vitamin A, Vitamin C")
    vitamins_ta = models.CharField(max_length=255, blank=True)
    vitamins_hi = models.CharField(max_length=255, blank=True)
    minerals = models.CharField(max_length=255, blank=True, help_text="e.g., Iron, Calcium")
    minerals_ta = models.CharField(max_length=255, blank=True)
    minerals_hi = models.CharField(max_length=255, blank=True)
    hydration = models.CharField(max_length=120, blank=True, help_text="e.g., Drink 500ml water")
    hydration_ta = models.CharField(max_length=120, blank=True)
    hydration_hi = models.CharField(max_length=120, blank=True)
    benefits = models.CharField(max_length=255, blank=True, help_text="e.g., High protein, Muscle recovery")
    benefits_ta = models.CharField(max_length=255, blank=True)
    benefits_hi = models.CharField(max_length=255, blank=True)
    diet_type = models.CharField(max_length=24, choices=DIET_TYPE_CHOICES, blank=True)
    sugar = models.FloatField(blank=True, null=True, help_text="Sugar in grams")
    sodium = models.FloatField(blank=True, null=True, help_text="Sodium in milligrams")
    cholesterol = models.FloatField(blank=True, null=True, help_text="Cholesterol in milligrams")

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = 'Program Item'
        verbose_name_plural = 'Program Items'

    def __str__(self):
        return f"{self.title} (Day {self.day.day_number})"

    @property
    def translated_title(self):
        return get_localized_field_value(self, 'title')

    @property
    def translated_description(self):
        return get_localized_field_value(self, 'description')

    @property
    def translated_hydration(self):
        return get_localized_field_value(self, 'hydration')

    @property
    def translated_benefits(self):
        return get_localized_field_value(self, 'benefits')

    @property
    def translated_vitamins(self):
        return get_localized_field_value(self, 'vitamins')

    @property
    def translated_minerals(self):
        return get_localized_field_value(self, 'minerals')


class WorkoutItem(models.Model):
    WEIGHT_LOSS = 'weight_loss'
    WEIGHT_GAIN = 'weight_gain'
    GOAL_CHOICES = [
        (WEIGHT_LOSS, 'Weight Loss'),
        (WEIGHT_GAIN, 'Weight Gain'),
    ]

    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='workout_items', null=True, blank=True)
    title = models.CharField(max_length=200)
    title_ta = models.CharField(max_length=200, blank=True)
    title_hi = models.CharField(max_length=200, blank=True)
    # Images support JPG/PNG/WEBP/GIF uploads. Videos are optional and stream
    # from Cloudinary when configured, keeping SQLite limited to paths/URLs.
    image = models.ImageField(upload_to=cloudinary_upload_path('workout_images'), blank=True, null=True)
    video = cloudinary_or_file_field('video', 'workout_videos', blank=True, null=True)
    description = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    duration = models.CharField(max_length=100, blank=True)
    duration_ta = models.CharField(max_length=100, blank=True)
    duration_hi = models.CharField(max_length=100, blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_CHOICES)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = 'Workout Item'
        verbose_name_plural = 'Workout Items'

    def __str__(self):
        return f"{self.title} (Day {self.day.day_number})"

    @property
    def translated_title(self):
        return get_localized_field_value(self, 'title')

    @property
    def translated_description(self):
        return get_localized_field_value(self, 'description')

    @property
    def translated_duration(self):
        return get_localized_field_value(self, 'duration')

    def save(self, *args, **kwargs):
        if not self.duration:
            self.duration = SiteSettings.get_solo().workout_duration_label
        super().save(*args, **kwargs)


class DayMedia(models.Model):
    WORKOUT_VIDEO = 'workout_video'
    EXERCISE_GIF = 'exercise_gif'
    EXERCISE_IMAGE = 'exercise_image'
    MEAL_IMAGE = 'meal_image'
    MEDIA_TYPE_CHOICES = [
        (WORKOUT_VIDEO, _('Workout Video')),
        (EXERCISE_GIF, _('Exercise GIF')),
        (EXERCISE_IMAGE, _('Exercise Image')),
        (MEAL_IMAGE, _('Meal Image')),
    ]

    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='media_items')
    media_type = models.CharField(max_length=24, choices=MEDIA_TYPE_CHOICES)
    media_file = cloudinary_or_file_field('auto', 'day_media', blank=True, null=True)
    title = models.CharField(max_length=200)
    title_ta = models.CharField(max_length=200, blank=True)
    title_hi = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    description_ta = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = 'Day Media'
        verbose_name_plural = 'Day Media'

    def __str__(self):
        return f"{self.title} - {self.get_media_type_display()} (Day {self.day.day_number})"

    @property
    def translated_title(self):
        return get_localized_field_value(self, 'title')

    @property
    def translated_description(self):
        return get_localized_field_value(self, 'description')

    @property
    def is_video(self):
        return self.media_type == self.WORKOUT_VIDEO

    @property
    def is_exercise_demo(self):
        return self.media_type in {self.EXERCISE_GIF, self.EXERCISE_IMAGE}

    @property
    def is_meal_image(self):
        return self.media_type == self.MEAL_IMAGE


class WaterTarget(models.Model):
    WEIGHT_LOSS = 'weight_loss'
    WEIGHT_GAIN = 'weight_gain'
    GOAL_CHOICES = [
        (WEIGHT_LOSS, 'Weight Loss'),
        (WEIGHT_GAIN, 'Weight Gain'),
    ]

    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='water_targets', null=True, blank=True)
    target_amount = models.CharField(max_length=100)
    target_amount_ta = models.CharField(max_length=100, blank=True)
    target_amount_hi = models.CharField(max_length=100, blank=True)
    reminder_note = models.TextField(blank=True)
    reminder_note_ta = models.TextField(blank=True)
    reminder_note_hi = models.TextField(blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_CHOICES)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = 'Water Target'
        verbose_name_plural = 'Water Targets'

    def __str__(self):
        return f"{self.target_amount} (Day {self.day.day_number})"

    @property
    def translated_target_amount(self):
        return get_localized_field_value(self, 'target_amount')

    @property
    def translated_reminder_note(self):
        return get_localized_field_value(self, 'reminder_note')

    @property
    def reminder_interval_minutes(self):
        return SiteSettings.get_solo().water_reminder_interval
