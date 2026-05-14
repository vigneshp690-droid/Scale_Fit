from django.db import OperationalError, ProgrammingError

from .models import SiteTheme, SiteSettings, UserProfile
from .theme_options import DEFAULT_THEME, get_theme, get_theme_class


def active_site_theme(request):
    theme_slug = DEFAULT_THEME

    try:
        theme_slug = SiteTheme.get_active_slug()
    except (OperationalError, ProgrammingError):
        theme_slug = DEFAULT_THEME

    return {
        "active_theme": get_theme(theme_slug),
        "active_theme_slug": theme_slug,
        "active_theme_class": get_theme_class(theme_slug),
    }


def current_user_profile(request):
    profile = None

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except (UserProfile.DoesNotExist, OperationalError, ProgrammingError):
            profile = None

    return {
        "current_user_profile": profile,
    }


def global_site_settings(request):
    if hasattr(request, 'site_settings'):
        return {
            "site_settings": request.site_settings,
        }

    try:
        settings = SiteSettings.get_solo()
    except (OperationalError, ProgrammingError):
        settings = None

    return {
        "site_settings": settings,
    }
