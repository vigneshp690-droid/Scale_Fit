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

    ingredients = models.TextField(blank=True, help_text="Enter ingredients separated by commas or newlines")
    ingredients_ta = models.TextField(blank=True)
    ingredients_hi = models.TextField(blank=True)
    
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
    def translated_ingredients(self):
        return get_localized_field_value(self, 'ingredients')

    def get_ingredients_list(self):
        ingredients_text = self.translated_ingredients or ''
        if not ingredients_text:
            return []
        if '\n' in ingredients_text:
            return [i.strip() for i in ingredients_text.split('\n') if i.strip()]
        else:
            return [i.strip() for i in ingredients_text.split(',') if i.strip()]

    def get_display_ingredients_list(self):
        saved_ingredients = self.get_ingredients_list()
        if saved_ingredients:
            return saved_ingredients

        suggested_ingredients = {
            'apple with almond butter': ['Apple slices', 'Almond butter', 'Cinnamon', 'Chia seeds'],
            'avocado egg toast': ['Whole grain toast', 'Avocado', 'Egg', 'Lemon juice', 'Black pepper'],
            'avocado toast': ['Whole grain toast', 'Avocado', 'Cherry tomatoes', 'Lemon juice', 'Chili flakes'],
            'baked chicken thighs': ['Chicken thighs', 'Olive oil', 'Garlic', 'Paprika', 'Mixed vegetables'],
            'baked salmon': ['Salmon fillet', 'Lemon', 'Olive oil', 'Garlic', 'Steamed greens'],
            'beef stir fry': ['Lean beef strips', 'Bell peppers', 'Broccoli', 'Soy sauce', 'Brown rice'],
            'beef tacos': ['Lean beef', 'Corn tortillas', 'Lettuce', 'Tomatoes', 'Avocado'],
            'beef and pasta': ['Lean beef', 'Whole wheat pasta', 'Tomato sauce', 'Spinach', 'Parmesan'],
            'boiled eggs': ['Eggs', 'Sea salt', 'Black pepper', 'Cucumber slices'],
            'breakfast burrito': ['Whole wheat tortilla', 'Eggs', 'Black beans', 'Bell peppers', 'Salsa'],
            'cauliflower rice bowl': ['Cauliflower rice', 'Chicken breast', 'Avocado', 'Black beans', 'Salsa'],
            'celery and hummus': ['Celery sticks', 'Hummus', 'Paprika', 'Olive oil'],
            'cheese and crackers': ['Whole grain crackers', 'Cheese slices', 'Grapes', 'Mixed seeds'],
            'chia pudding': ['Chia seeds', 'Milk', 'Greek yogurt', 'Berries', 'Honey'],
            'chicken burrito bowl': ['Chicken breast', 'Brown rice', 'Black beans', 'Corn', 'Salsa'],
            'chicken pasta': ['Chicken breast', 'Whole wheat pasta', 'Tomato sauce', 'Spinach', 'Parmesan'],
            'chicken rice bowl': ['Chicken breast', 'Brown rice', 'Broccoli', 'Carrots', 'Sesame seeds'],
            'chicken stir fry': ['Chicken breast', 'Mixed vegetables', 'Soy sauce', 'Garlic', 'Brown rice'],
            'cottage cheese bowl': ['Cottage cheese', 'Berries', 'Banana', 'Granola', 'Honey'],
            'cucumber slices': ['Cucumber', 'Lemon juice', 'Sea salt', 'Black pepper'],
            'eggs and steak': ['Eggs', 'Lean steak', 'Spinach', 'Mushrooms', 'Olive oil'],
            'french toast': ['Whole grain bread', 'Eggs', 'Milk', 'Cinnamon', 'Berries'],
            'greek yogurt': ['Greek yogurt', 'Berries', 'Granola', 'Honey'],
            'greek yogurt parfait': ['Greek yogurt', 'Granola', 'Kiwi', 'Blueberries', 'Banana', 'Honey'],
            'green smoothie bowl': ['Spinach', 'Banana', 'Greek yogurt', 'Protein powder', 'Granola'],
            'grilled chicken salad': ['Grilled chicken', 'Mixed greens', 'Cucumber', 'Tomatoes', 'Olive oil dressing'],
            'grilled tilapia': ['Tilapia fillet', 'Lemon', 'Garlic', 'Quinoa', 'Green beans'],
            'lamb chops': ['Lamb chops', 'Rosemary', 'Garlic', 'Sweet potato', 'Green salad'],
            'lentil soup': ['Lentils', 'Carrots', 'Celery', 'Tomatoes', 'Vegetable broth'],
            'mass gainer smoothie': ['Milk', 'Banana', 'Peanut butter', 'Oats', 'Protein powder'],
            'milk and cookies': ['Milk', 'Oat cookies', 'Peanut butter', 'Cinnamon'],
            'mixed nuts': ['Almonds', 'Walnuts', 'Cashews', 'Pumpkin seeds'],
            'oatmeal power bowl': ['Oats', 'Milk', 'Banana', 'Peanut butter', 'Chia seeds'],
            'oatmeal with berries': ['Oats', 'Milk', 'Blueberries', 'Strawberries', 'Honey'],
            'peanut butter banana': ['Banana', 'Peanut butter', 'Chia seeds', 'Cinnamon'],
            'pork tenderloin': ['Pork tenderloin', 'Garlic', 'Rosemary', 'Sweet potato', 'Green beans'],
            'protein pancake stack': ['Protein pancake mix', 'Eggs', 'Milk', 'Banana', 'Berries'],
            'protein shake': ['Protein powder', 'Milk', 'Banana', 'Ice'],
            'protein smoothie': ['Protein powder', 'Greek yogurt', 'Banana', 'Berries', 'Milk'],
            'quinoa buddha bowl': ['Quinoa', 'Chickpeas', 'Avocado', 'Roasted vegetables', 'Tahini dressing'],
            'rice cakes': ['Rice cakes', 'Peanut butter', 'Banana slices', 'Cinnamon'],
            'salmon quinoa bowl': ['Salmon', 'Quinoa', 'Avocado', 'Cucumber', 'Lemon dressing'],
            'salmon and rice': ['Salmon', 'Brown rice', 'Broccoli', 'Lemon', 'Sesame seeds'],
            'shrimp tacos': ['Shrimp', 'Corn tortillas', 'Cabbage slaw', 'Avocado', 'Lime'],
            'steak and potatoes': ['Lean steak', 'Potatoes', 'Asparagus', 'Garlic', 'Olive oil'],
            'stuffed chicken breast': ['Chicken breast', 'Spinach', 'Low-fat cheese', 'Garlic', 'Quinoa'],
            'trail mix': ['Almonds', 'Walnuts', 'Dried fruit', 'Pumpkin seeds', 'Dark chocolate chips'],
            'tuna pasta salad': ['Tuna', 'Whole wheat pasta', 'Cucumber', 'Cherry tomatoes', 'Greek yogurt dressing'],
            'tuna stuffed peppers': ['Bell peppers', 'Tuna', 'Greek yogurt', 'Celery', 'Brown rice'],
            'turkey lettuce wraps': ['Turkey slices', 'Lettuce leaves', 'Avocado', 'Cucumber', 'Hummus'],
            'turkey meatballs': ['Lean turkey', 'Egg', 'Breadcrumbs', 'Tomato sauce', 'Zucchini noodles'],
            'turkey sub': ['Whole grain sub roll', 'Turkey slices', 'Lettuce', 'Tomato', 'Mustard'],
            'vegetable curry': ['Mixed vegetables', 'Chickpeas', 'Coconut milk', 'Curry spices', 'Brown rice'],
            'veggie omelette': ['Eggs', 'Spinach', 'Bell peppers', 'Mushrooms', 'Low-fat cheese'],
            'whole grain pancakes': ['Whole grain flour', 'Eggs', 'Milk', 'Berries', 'Maple syrup'],
            'zucchini noodles': ['Zucchini noodles', 'Tomato sauce', 'Turkey meatballs', 'Parmesan', 'Basil'],
        }
        ingredients = suggested_ingredients.get((self.title or '').strip().lower(), [])
        language_code = (get_language() or 'en').split('-')[0]
        ingredient_translations = {
            'ta': {
                'Apple slices': 'ஆப்பிள் துண்டுகள்',
                'Almond butter': 'பாதாம் வெண்ணெய்',
                'Cinnamon': 'இலவங்கப்பட்டை',
                'Chia seeds': 'சியா விதைகள்',
                'Whole grain toast': 'முழு தானிய டோஸ்ட்',
                'Avocado': 'அவகாடோ',
                'Egg': 'முட்டை',
                'Eggs': 'முட்டைகள்',
                'Lemon juice': 'எலுமிச்சை சாறு',
                'Black pepper': 'கருப்பு மிளகு',
                'Cherry tomatoes': 'செர்ரி தக்காளி',
                'Chili flakes': 'மிளகாய் துகள்கள்',
                'Chicken thighs': 'கோழி தொடைகள்',
                'Chicken breast': 'கோழி மார்பு',
                'Olive oil': 'ஆலிவ் எண்ணெய்',
                'Garlic': 'பூண்டு',
                'Paprika': 'பாப்ரிகா',
                'Mixed vegetables': 'கலவை காய்கறிகள்',
                'Salmon fillet': 'சால்மன் மீன் துண்டு',
                'Salmon': 'சால்மன்',
                'Lemon': 'எலுமிச்சை',
                'Steamed greens': 'ஆவியில் வேகவைத்த கீரைகள்',
                'Lean beef strips': 'கொழுப்பு குறைந்த மாட்டிறைச்சி துண்டுகள்',
                'Lean beef': 'கொழுப்பு குறைந்த மாட்டிறைச்சி',
                'Bell peppers': 'குடைமிளகாய்',
                'Broccoli': 'ப்ரோக்கோலி',
                'Soy sauce': 'சோயா சாஸ்',
                'Brown rice': 'பழுப்பு அரிசி',
                'Corn tortillas': 'சோள டோர்டில்லா',
                'Lettuce': 'லெட்டூஸ்',
                'Tomato': 'தக்காளி',
                'Tomatoes': 'தக்காளி',
                'Whole wheat pasta': 'முழு கோதுமை பாஸ்தா',
                'Tomato sauce': 'தக்காளி சாஸ்',
                'Spinach': 'கீரை',
                'Parmesan': 'பார்மசான் சீஸ்',
                'Sea salt': 'கடல் உப்பு',
                'Cucumber slices': 'வெள்ளரிக்காய் துண்டுகள்',
                'Whole wheat tortilla': 'முழு கோதுமை டோர்டில்லா',
                'Black beans': 'கருப்பு பீன்ஸ்',
                'Salsa': 'சால்சா',
                'Cauliflower rice': 'காலிஃபிளவர் அரிசி',
                'Celery sticks': 'செலரி குச்சிகள்',
                'Hummus': 'ஹம்மஸ்',
                'Whole grain crackers': 'முழு தானிய கிராக்கர்கள்',
                'Cheese slices': 'சீஸ் துண்டுகள்',
                'Grapes': 'திராட்சை',
                'Mixed seeds': 'கலவை விதைகள்',
                'Milk': 'பால்',
                'Greek yogurt': 'கிரீக் யோகர்ட்',
                'Berries': 'பெர்ரி பழங்கள்',
                'Honey': 'தேன்',
                'Corn': 'சோளம்',
                'Carrots': 'கேரட்',
                'Sesame seeds': 'எள்',
                'Cottage cheese': 'காட்டேஜ் சீஸ்',
                'Banana': 'வாழைப்பழம்',
                'Granola': 'கிரனோலா',
                'Cucumber': 'வெள்ளரிக்காய்',
                'Lean steak': 'கொழுப்பு குறைந்த ஸ்டேக்',
                'Mushrooms': 'காளான்',
                'Whole grain bread': 'முழு தானிய ரொட்டி',
                'Kiwi': 'கிவி',
                'Blueberries': 'ப்ளூபெர்ரி',
                'Protein powder': 'புரதப் பொடி',
                'Grilled chicken': 'கிரில் செய்த கோழி',
                'Mixed greens': 'கலவை கீரைகள்',
                'Olive oil dressing': 'ஆலிவ் எண்ணெய் டிரெஸ்ஸிங்',
                'Tilapia fillet': 'திலாபியா மீன் துண்டு',
                'Quinoa': 'கினோவா',
                'Green beans': 'பச்சை பீன்ஸ்',
                'Lamb chops': 'ஆட்டிறைச்சி சாப்ஸ்',
                'Rosemary': 'ரோஸ்மேரி',
                'Sweet potato': 'சர்க்கரைவள்ளி கிழங்கு',
                'Green salad': 'பச்சை சாலட்',
                'Lentils': 'பருப்பு',
                'Celery': 'செலரி',
                'Vegetable broth': 'காய்கறி சூப் நீர்',
                'Peanut butter': 'வேர்க்கடலை வெண்ணெய்',
                'Oats': 'ஓட்ஸ்',
                'Oat cookies': 'ஓட்ஸ் குக்கீஸ்',
                'Almonds': 'பாதாம்',
                'Walnuts': 'வால்நட்',
                'Cashews': 'முந்திரி',
                'Pumpkin seeds': 'பூசணி விதைகள்',
                'Blueberries': 'ப்ளூபெர்ரி',
                'Strawberries': 'ஸ்ட்ராபெர்ரி',
                'Pork tenderloin': 'பன்றி டெண்டர்லோயின்',
                'Protein pancake mix': 'புரத பான்கேக் கலவை',
                'Ice': 'ஐஸ்',
                'Chickpeas': 'கொண்டைக்கடலை',
                'Roasted vegetables': 'வறுத்த காய்கறிகள்',
                'Tahini dressing': 'தஹினி டிரெஸ்ஸிங்',
                'Rice cakes': 'அரிசி கேக்குகள்',
                'Banana slices': 'வாழைப்பழ துண்டுகள்',
                'Lemon dressing': 'எலுமிச்சை டிரெஸ்ஸிங்',
                'Shrimp': 'இறால்',
                'Cabbage slaw': 'முட்டைகோஸ் ஸ்லா',
                'Lime': 'லைம்',
                'Potatoes': 'உருளைக்கிழங்கு',
                'Asparagus': 'அஸ்பாரகஸ்',
                'Low-fat cheese': 'குறைந்த கொழுப்பு சீஸ்',
                'Dried fruit': 'உலர் பழங்கள்',
                'Dark chocolate chips': 'டார்க் சாக்லேட் சிப்ஸ்',
                'Tuna': 'டூனா மீன்',
                'Cherry tomatoes': 'செர்ரி தக்காளி',
                'Greek yogurt dressing': 'கிரீக் யோகர்ட் டிரெஸ்ஸிங்',
                'Lean turkey': 'கொழுப்பு குறைந்த டர்கி',
                'Turkey slices': 'டர்கி துண்டுகள்',
                'Lettuce leaves': 'லெட்டூஸ் இலைகள்',
                'Turkey meatballs': 'டர்கி மீட்பால்ஸ்',
                'Breadcrumbs': 'ரொட்டி தூள்',
                'Zucchini noodles': 'சுக்கினி நூடுல்ஸ்',
                'Whole grain sub roll': 'முழு தானிய சப் ரோல்',
                'Mustard': 'மஸ்டர்ட்',
                'Coconut milk': 'தேங்காய் பால்',
                'Curry spices': 'கறி மசாலா',
                'Whole grain flour': 'முழு தானிய மாவு',
                'Maple syrup': 'மேபிள் சிரப்',
                'Basil': 'துளசி',
            },
            'hi': {
                'Apple slices': 'सेब के टुकड़े',
                'Almond butter': 'बादाम बटर',
                'Cinnamon': 'दालचीनी',
                'Chia seeds': 'चिया बीज',
                'Whole grain toast': 'साबुत अनाज टोस्ट',
                'Avocado': 'एवोकाडो',
                'Egg': 'अंडा',
                'Eggs': 'अंडे',
                'Lemon juice': 'नींबू का रस',
                'Black pepper': 'काली मिर्च',
                'Cherry tomatoes': 'चेरी टमाटर',
                'Chili flakes': 'मिर्च फ्लेक्स',
                'Chicken thighs': 'चिकन थाई',
                'Chicken breast': 'चिकन ब्रेस्ट',
                'Olive oil': 'जैतून का तेल',
                'Garlic': 'लहसुन',
                'Paprika': 'पाप्रिका',
                'Mixed vegetables': 'मिश्रित सब्जियां',
                'Salmon fillet': 'सैल्मन फिले',
                'Salmon': 'सैल्मन',
                'Lemon': 'नींबू',
                'Steamed greens': 'भाप में पकी हरी सब्जियां',
                'Lean beef strips': 'लीन बीफ स्ट्रिप्स',
                'Lean beef': 'लीन बीफ',
                'Bell peppers': 'शिमला मिर्च',
                'Broccoli': 'ब्रोकली',
                'Soy sauce': 'सोया सॉस',
                'Brown rice': 'ब्राउन राइस',
                'Corn tortillas': 'कॉर्न टॉर्टिला',
                'Lettuce': 'लेट्यूस',
                'Tomato': 'टमाटर',
                'Tomatoes': 'टमाटर',
                'Whole wheat pasta': 'होल व्हीट पास्ता',
                'Tomato sauce': 'टमाटर सॉस',
                'Spinach': 'पालक',
                'Parmesan': 'पार्मेज़ान चीज',
                'Sea salt': 'समुद्री नमक',
                'Cucumber slices': 'खीरे के टुकड़े',
                'Whole wheat tortilla': 'होल व्हीट टॉर्टिला',
                'Black beans': 'ब्लैक बीन्स',
                'Salsa': 'साल्सा',
                'Cauliflower rice': 'फूलगोभी राइस',
                'Celery sticks': 'सेलेरी स्टिक्स',
                'Hummus': 'हमस',
                'Whole grain crackers': 'साबुत अनाज क्रैकर्स',
                'Cheese slices': 'चीज स्लाइस',
                'Grapes': 'अंगूर',
                'Mixed seeds': 'मिश्रित बीज',
                'Milk': 'दूध',
                'Greek yogurt': 'ग्रीक योगर्ट',
                'Berries': 'बेरी',
                'Honey': 'शहद',
                'Corn': 'मक्का',
                'Carrots': 'गाजर',
                'Sesame seeds': 'तिल',
                'Cottage cheese': 'कॉटेज चीज',
                'Banana': 'केला',
                'Granola': 'ग्रेनोला',
                'Cucumber': 'खीरा',
                'Lean steak': 'लीन स्टेक',
                'Mushrooms': 'मशरूम',
                'Whole grain bread': 'साबुत अनाज ब्रेड',
                'Kiwi': 'कीवी',
                'Blueberries': 'ब्लूबेरी',
                'Protein powder': 'प्रोटीन पाउडर',
                'Grilled chicken': 'ग्रिल्ड चिकन',
                'Mixed greens': 'मिश्रित हरी पत्तियां',
                'Olive oil dressing': 'जैतून तेल ड्रेसिंग',
                'Tilapia fillet': 'तिलापिया फिले',
                'Quinoa': 'क्विनोआ',
                'Green beans': 'हरी बीन्स',
                'Lamb chops': 'लैम्ब चॉप्स',
                'Rosemary': 'रोजमेरी',
                'Sweet potato': 'शकरकंद',
                'Green salad': 'ग्रीन सलाद',
                'Lentils': 'दाल',
                'Celery': 'सेलेरी',
                'Vegetable broth': 'सब्जी शोरबा',
                'Peanut butter': 'पीनट बटर',
                'Oats': 'ओट्स',
                'Oat cookies': 'ओट कुकीज़',
                'Almonds': 'बादाम',
                'Walnuts': 'अखरोट',
                'Cashews': 'काजू',
                'Pumpkin seeds': 'कद्दू के बीज',
                'Strawberries': 'स्ट्रॉबेरी',
                'Pork tenderloin': 'पोर्क टेंडरलॉइन',
                'Protein pancake mix': 'प्रोटीन पैनकेक मिक्स',
                'Ice': 'बर्फ',
                'Chickpeas': 'चना',
                'Roasted vegetables': 'भुनी हुई सब्जियां',
                'Tahini dressing': 'ताहिनी ड्रेसिंग',
                'Rice cakes': 'राइस केक',
                'Banana slices': 'केले के टुकड़े',
                'Lemon dressing': 'नींबू ड्रेसिंग',
                'Shrimp': 'झींगा',
                'Cabbage slaw': 'पत्ता गोभी स्लॉ',
                'Lime': 'लाइम',
                'Potatoes': 'आलू',
                'Asparagus': 'एस्पैरागस',
                'Low-fat cheese': 'लो-फैट चीज',
                'Dried fruit': 'सूखे फल',
                'Dark chocolate chips': 'डार्क चॉकलेट चिप्स',
                'Tuna': 'टूना',
                'Greek yogurt dressing': 'ग्रीक योगर्ट ड्रेसिंग',
                'Lean turkey': 'लीन टर्की',
                'Turkey slices': 'टर्की स्लाइस',
                'Lettuce leaves': 'लेट्यूस पत्ते',
                'Turkey meatballs': 'टर्की मीटबॉल्स',
                'Breadcrumbs': 'ब्रेडक्रम्ब्स',
                'Zucchini noodles': 'ज़ुकीनी नूडल्स',
                'Whole grain sub roll': 'साबुत अनाज सब रोल',
                'Mustard': 'मस्टर्ड',
                'Coconut milk': 'नारियल दूध',
                'Curry spices': 'करी मसाले',
                'Whole grain flour': 'साबुत अनाज आटा',
                'Maple syrup': 'मेपल सिरप',
                'Basil': 'तुलसी',
            },
        }
        translations = ingredient_translations.get(language_code, {})
        return [translations.get(ingredient, ingredient) for ingredient in ingredients]

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
