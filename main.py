import random
import string

from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponseNotFound
from django.urls import path
from django.shortcuts import render
from django.shortcuts import redirect

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


# def url_redirect(request, key):
#     for l1, l2 in request.POST.items():
#         link = l2
#     return redirect(link)


def url_shortener(request):
    print(request.POST)
    letters = string.ascii_letters
    rand_key = ''.join(random.choice(letters) for i in range(5))

    if request.POST:
        for l1, l2 in request.POST.items():
            key = l1
            link = l2
        if link.split(':')[0] != 'https':
            return render(request, "result.html", {'i': 1})
        return render(request, "result.html", {'key': key,
                                               'link': link,
                                               'rand_key': rand_key})

    return render(request, "main.html", {'rand_key': rand_key})


urlpatterns = [
    path('url', url_shortener),
    # path('url/<key>', url_redirect, name='url_redirect')
]

if __name__ == '__main__':
    execute_from_command_line()

# нерабочая строка кода из 'result.html':
# <h1><a href="{% url 'url_redirect' key %}"> {{ rand_key }} </a> </h1>