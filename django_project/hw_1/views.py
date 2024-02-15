from django.shortcuts import render

# Create your views here.

import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def decologger(func):
    def wrapper(request, *args, **kwargs):
        logger.info(f"{func.__name__} page was requested.")
        return func(request, *args, **kwargs)
    return wrapper


@decologger
def main(request):
    title = "Главная страница"
    content = "Тут могла бы быть ваша реклама."
    nav = [("Главная", "../main/"),
           ("Обо мне", "../about/")]
    response = (f"<h1>{title}</h1>"
                f"<p>{content}</p>"
                f"<ul>{''.join(f'<li><a href="{link}">{name}</a></li>' for name, link in nav)}</ul>")
    return HttpResponse(response)


@decologger
def about(request):
    title = "Страница обо мне"
    content = "Какие-то очень интересные данные обо мне."
    nav = [("Главная", "../main/"),
           ("Обо мне", "../about/")]
    response = (f"<h1>{title}</h1>"
                f"<p>{content}</p>"
                f"<ul>{''.join(f'<li><a href="{link}">{name}</a></li>' for name, link in nav)}</ul>")
    return HttpResponse(response)
