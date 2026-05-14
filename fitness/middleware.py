from django.db import OperationalError, ProgrammingError
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
            selected_language = request.session.get(LANGUAGE_SESSION_KEY) or translation.get_language_from_request(request)
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
