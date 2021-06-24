import random

from urllib.parse import urlparse
from django.conf import settings
from django.core.cache import cache
from django.core.management import execute_from_command_line
from django.urls import path
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.baseconv import base56

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='secret',
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [''],
        }
    ]
)

ALLOWED_SCHEMES = {'http', 'https', 'ftp'}
MIN_KEY, MAX_KEY = 80106440, 550731775


def url_redirect(request, key):
    return redirect(to=cache.get(key, '/'))


def url_shortener(request):
    ctx = {}
    if request.POST:
        url = request.POST.get('url')
        if urlparse(url).scheme in ALLOWED_SCHEMES:
            key = base56.encode(random.randint(MIN_KEY, MAX_KEY))
            cache.add(key, url)
            ctx['key'] = key
        else:
            ctx['message'] = f'Invalid URL {url}. Allowed schemes: ' + ','.join(ALLOWED_SCHEMES)
    return render(request, 'result.html', ctx)


urlpatterns = [
    path('url', url_shortener),
    path('url/<key>', url_redirect, name='url_redirect')
]

if __name__ == '__main__':
    execute_from_command_line()

