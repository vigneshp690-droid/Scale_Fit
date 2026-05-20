from django.contrib import admin
from django.utils.html import format_html
from .media_storage import optimized_cloudinary_url
from .models import UserProfile, SiteSettings, Program, Plan, Day, ProgramItem, WorkoutItem, DayMedia, WaterTarget


def media_link(field_file):
    if not field_file:
        return 'No media'
    url = optimized_cloudinary_url(field_file)
    return format_html('<a href="{}" target="_blank" rel="noopener">{}</a>', url, url)


def image_preview(field_file, alt_text):
    if not field_file:
        return 'No image'
    url = optimized_cloudinary_url(field_file, width=320)
    return format_html(
        '<a href="{}" target="_blank" rel="noopener">'
        '<img src="{}" alt="{}" style="width:72px;height:54px;border-radius:8px;object-fit:cover;" />'
        '</a>',
        optimized_cloudinary_url(field_file),
        url,
        alt_text,
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'default_workout_duration', 'publishing_mode', 'default_language', 'currency', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Program Settings', {
            'fields': (
                'default_workout_duration', 'meal_timing_preference', 'water_reminder_interval',
                'publishing_mode', 'enable_weight_loss_programs', 'enable_weight_gain_programs',
                'auto_publish_programs',
            )
        }),
        ('Language & Region', {
            'fields': ('default_language', 'timezone', 'date_format', 'measurement_unit', 'currency', 'region')
        }),
        ('Support', {
            'fields': ('support_email', 'support_phone', 'support_working_hours', 'help_center_url', 'enable_live_chat')
        }),
        ('Notifications', {
            'fields': (
                'enable_email_notifications', 'enable_push_notifications',
                'enable_water_reminders', 'enable_admin_alerts',
            )
        }),
        ('User Website Appearance', {
            'fields': ('primary_theme_color', 'secondary_theme_color', 'enable_dark_mode', 'site_logo', 'favicon')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number', 'profile_image_preview', 'trainer_image_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'mobile_number')
    readonly_fields = ('profile_image_preview', 'trainer_image_preview', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Details', {
            'fields': ('mobile_number',)
        }),
        ('Media', {
            'fields': ('profile_image', 'profile_image_preview', 'trainer_image', 'trainer_image_preview')
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def profile_image_preview(self, obj):
        if not obj.profile_image:
            return 'No image'

        return format_html(
            '<a href="{}" target="_blank" rel="noopener">'
            '<img src="{}" alt="{} profile image" style="width:48px;height:48px;border-radius:50%;object-fit:cover;" />'
            '</a>',
            obj.profile_image.url,
            obj.profile_image.url,
            obj.user.username,
        )

    profile_image_preview.short_description = 'Profile image'

    def trainer_image_preview(self, obj):
        if not obj.trainer_image:
            return 'No image'

        return format_html(
            '<a href="{}" target="_blank" rel="noopener">'
            '<img src="{}" alt="{} trainer image" style="width:48px;height:48px;border-radius:8px;object-fit:cover;" />'
            '</a>',
            obj.trainer_image.url,
            obj.trainer_image.url,
            obj.user.username,
        )

    trainer_image_preview.short_description = 'Trainer image'


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'goal_type', 'is_active', 'created_at')
    list_filter = ('goal_type', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'goal_type', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'plan_type', 'count', 'is_active', 'created_at')
    list_filter = ('program__goal_type', 'plan_type', 'is_active')
    search_fields = ('name', 'program__name', 'description')
    ordering = ('program', 'plan_type')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('program', 'name', 'plan_type', 'count', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('title', 'plan', 'day_number', 'is_active', 'created_at')
    list_filter = ('plan__program__goal_type', 'plan', 'is_active')
    search_fields = ('title', 'plan__name', 'description')
    ordering = ('plan', 'day_number')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('plan', 'day_number', 'title', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProgramItem)
class ProgramItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'day', 'meal_category', 'media_status', 'display_order', 'is_active', 'created_at')
    list_filter = ('day__plan__program__goal_type', 'meal_category', 'is_active')
    search_fields = ('title', 'description', 'day__plan__name')
    ordering = ('day__plan', 'day__day_number', 'display_order')
    list_editable = ('display_order', 'is_active')
    readonly_fields = ('image_preview', 'video_preview', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('day', 'title', 'image', 'image_preview', 'video', 'video_preview', 'description')
        }),
        ('Program Settings', {
            'fields': ('meal_category', 'display_order', 'is_active')
        }),
        ('Nutritional Information', {
            'fields': ('calories', 'protein', 'carbs', 'fat', 'fiber', 'vitamins', 'minerals')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        return image_preview(obj.image, f'{obj.title} meal image')

    def video_preview(self, obj):
        return media_link(obj.video)

    def media_status(self, obj):
        labels = []
        if obj.image:
            labels.append('Image/GIF')
        if obj.video:
            labels.append('Video')
        return ', '.join(labels) if labels else 'No media'

    image_preview.short_description = 'Current image/GIF'
    video_preview.short_description = 'Current video'
    media_status.short_description = 'Media'


@admin.register(WorkoutItem)
class WorkoutItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'day', 'duration', 'media_status', 'display_order', 'is_active', 'created_at')
    list_filter = ('day__plan__program__goal_type', 'is_active')
    search_fields = ('title', 'description', 'day__plan__name')
    ordering = ('day__plan', 'day__day_number', 'display_order')
    list_editable = ('display_order', 'is_active')
    readonly_fields = ('image_preview', 'video_preview', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('day', 'title', 'image', 'image_preview', 'video', 'video_preview', 'description')
        }),
        ('Workout Settings', {
            'fields': ('duration', 'display_order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        return image_preview(obj.image, f'{obj.title} workout image')

    def video_preview(self, obj):
        return media_link(obj.video)

    def media_status(self, obj):
        labels = []
        if obj.image:
            labels.append('Image/GIF')
        if obj.video:
            labels.append('Video')
        return ', '.join(labels) if labels else 'No media'

    image_preview.short_description = 'Current image/GIF'
    video_preview.short_description = 'Current video'
    media_status.short_description = 'Media'


@admin.register(DayMedia)
class DayMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'day', 'media_type', 'media_link_preview', 'display_order', 'is_active', 'created_at')
    list_filter = ('day__plan__program__goal_type', 'media_type', 'is_active')
    search_fields = ('title', 'description', 'day__title', 'day__plan__name')
    ordering = ('day__plan', 'day__day_number', 'display_order')
    list_editable = ('display_order', 'is_active')
    readonly_fields = ('media_link_preview', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('day', 'media_type', 'title', 'media_file', 'media_link_preview', 'description')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def media_link_preview(self, obj):
        return media_link(obj.media_file)

    media_link_preview.short_description = 'Current media'


@admin.register(WaterTarget)
class WaterTargetAdmin(admin.ModelAdmin):
    list_display = ('target_amount', 'day', 'display_order', 'is_active', 'created_at')
    list_filter = ('day__plan__program__goal_type', 'is_active')
    search_fields = ('target_amount', 'reminder_note', 'day__plan__name')
    ordering = ('day__plan', 'day__day_number', 'display_order')
    list_editable = ('display_order', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('day', 'target_amount', 'reminder_note', 'display_order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
