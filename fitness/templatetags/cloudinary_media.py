from django import template

from fitness.media_storage import optimized_cloudinary_url


register = template.Library()


@register.filter
def optimized_media_url(field_file, width=None):
    """Return a q_auto/f_auto Cloudinary URL, or the legacy local media URL."""
    return optimized_cloudinary_url(field_file, width=width)


@register.filter
def video_media_url(field_file):
    """Return a browser-playable MP4 URL for Cloudinary/local video fields."""
    return optimized_cloudinary_url(field_file, resource_type='video')


@register.simple_tag
def responsive_image_srcset(field_file, widths='320,640,960,1280'):
    """Generate responsive Cloudinary srcset entries while preserving local fallback URLs."""
    srcset = []
    for raw_width in str(widths).split(','):
        width = raw_width.strip()
        if width.isdigit():
            srcset.append(f'{optimized_cloudinary_url(field_file, width=int(width))} {width}w')
    return ', '.join(srcset)
