from pathlib import PurePosixPath

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import filepath_to_uri


CLOUDINARY_UPLOAD_PREFIX = 'cloudinary'
VIDEO_EXTENSIONS = ('.mp4', '.webm', '.mov', '.m4v', '.avi', '.mkv')


def cloudinary_upload_path(folder):
    """Store new uploads under a marker prefix so legacy local paths stay local."""
    return f'{CLOUDINARY_UPLOAD_PREFIX}/{folder}/'


def is_remote_media_name(name):
    value = str(name or '')
    return value.startswith('http://') or value.startswith('https://')


def is_cloudinary_media_name(name):
    value = str(name or '').lstrip('/')
    return value.startswith(f'{CLOUDINARY_UPLOAD_PREFIX}/')


def get_media_resource_type(name):
    suffix = PurePosixPath(str(name or '')).suffix.lower()
    if suffix in VIDEO_EXTENSIONS:
        return 'video'
    return 'image'


def get_media_identifier(media):
    if hasattr(media, 'public_id') and media.public_id:
        return media.public_id
    if hasattr(media, 'name') and media.name:
        return media.name
    return media


def get_media_direct_url(media):
    try:
        return str(media.url or '')
    except Exception:
        return ''


def find_local_media_with_extension(value, resource_type):
    if resource_type != 'video':
        return ''
    if PurePosixPath(value).suffix:
        return ''

    for extension in VIDEO_EXTENSIONS:
        candidate = f'{value}{extension}'
        if (settings.MEDIA_ROOT / candidate).exists():
            return f'{settings.MEDIA_URL}{filepath_to_uri(candidate)}'
    return ''


def optimized_cloudinary_url(media, width=None, height=None, crop='fill', resource_type=None):
    """
    Build optimized delivery URLs for Cloudinary-backed media.

    Images use q_auto/f_auto for automatic compression and format selection.
    Videos use q_auto/f_auto so Cloudinary can deliver a streaming-friendly
    format while the database stores only the Cloudinary path or URL.
    """
    direct_url = get_media_direct_url(media)
    explicit_resource_type = resource_type or getattr(media, 'resource_type', None)
    value = str(get_media_identifier(media) or '')
    if not value:
        return direct_url

    if is_remote_media_name(value):
        return value

    if direct_url and not is_remote_media_name(direct_url) and not is_remote_media_name(value):
        return direct_url

    resolved_resource_type = explicit_resource_type or get_media_resource_type(value)
    local_video_url = find_local_media_with_extension(value, resolved_resource_type)
    if local_video_url:
        return local_video_url

    if value.startswith(settings.MEDIA_URL):
        return value

    if not is_cloudinary_media_name(value):
        return f'{settings.MEDIA_URL}{filepath_to_uri(value)}'

    try:
        from cloudinary.utils import cloudinary_url
    except ImportError:
        return value

    public_id = value

    options = {
        'secure': True,
        'resource_type': resolved_resource_type,
        'quality': 'auto',
    }
    if resolved_resource_type == 'video':
        options['format'] = 'mp4'
    else:
        options['fetch_format'] = 'auto'
    if width:
        options['width'] = width
        options['crop'] = crop
    if height:
        options['height'] = height

    try:
        return cloudinary_url(public_id, **options)[0]
    except Exception:
        return direct_url or local_video_url or value


class ScaleFitCloudinaryMediaStorage(FileSystemStorage):
    """
    Backward-compatible Cloudinary media storage.

    Existing SQLite rows contain local relative paths. New uploads are saved to
    Cloudinary when credentials are configured, while old paths continue to be
    served from MEDIA_ROOT during development.
    """

    def __init__(self, *args, **kwargs):
        self._cloudinary_storage = None
        try:
            from cloudinary_storage.storage import MediaCloudinaryStorage
        except ImportError:
            pass
        else:
            self._cloudinary_storage = MediaCloudinaryStorage()
        super().__init__(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)

    def _save(self, name, content):
        if self._cloudinary_storage and is_cloudinary_media_name(name):
            return self._cloudinary_storage.save(name, content)
        return super()._save(name, content)

    def delete(self, name):
        if self._cloudinary_storage and (is_cloudinary_media_name(name) or is_remote_media_name(name)):
            self._cloudinary_storage.delete(name)
            return
        super().delete(name)

    def exists(self, name):
        if self._cloudinary_storage and is_cloudinary_media_name(name):
            return False
        return super().exists(name)

    def url(self, name):
        if self._cloudinary_storage and (is_cloudinary_media_name(name) or is_remote_media_name(name)):
            return optimized_cloudinary_url(name)
        return super().url(name)
