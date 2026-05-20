from django.db import OperationalError, ProgrammingError
from django.conf import settings as django_settings
from django.utils import timezone, translation

from .models import SiteSettings


USER_SITE_PREFIX = '/site/'
LANGUAGE_SESSION_KEY = 'django_language'


class SiteSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_user_site = request.path == '/' or request.path.startswith(USER_SITE_PREFIX)

        try:
            settings = SiteSettings.get_solo()
            timezone.activate(settings.timezone)
            session = getattr(request, 'session', {})
            session_language = session.get(LANGUAGE_SESSION_KEY) if hasattr(session, 'get') else None
            cookie_language = request.COOKIES.get(django_settings.LANGUAGE_COOKIE_NAME)
            selected_language = session_language or cookie_language
            language_code = selected_language or (settings.default_language if is_user_site else 'en')
            translation.activate(language_code)
            request.LANGUAGE_CODE = language_code
            request.site_settings = settings
        except (OperationalError, ProgrammingError):
            request.site_settings = None

        response = self.get_response(request)
        translation.deactivate()
        timezone.deactivate()
        return response
