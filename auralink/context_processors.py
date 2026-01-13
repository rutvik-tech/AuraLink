import os
from pathlib import Path
from django.conf import settings


def _find_static_image(base_dir: Path, candidates):
    for name in candidates:
        p = base_dir / 'static' / 'images' / name
        if p.exists():
            return f"/static/images/{name}"
    return None


def site_settings(request):
    base_dir = Path(settings.BASE_DIR)

    hero = _find_static_image(base_dir, ['hero.jpg', 'Hero.jpg', 'hero.png', 'hero.svg', 'Hero.png'])
    logo = _find_static_image(base_dir, ['logo.png', 'Logo.png', 'logo.svg', 'Logo.svg'])
    favicon = _find_static_image(base_dir, ['favicon.ico', 'favicon.png', 'favicon.svg'])

    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'AuraLink'),
        'HERO_IMAGE_URL': hero or getattr(settings, 'HERO_IMAGE_URL', '/static/images/hero.jpg'),
        'LOGO_URL': logo or getattr(settings, 'LOGO_URL', '/static/images/logo.png'),
        'FAVICON_URL': favicon or getattr(settings, 'FAVICON_URL', '/static/images/favicon.svg'),
    }