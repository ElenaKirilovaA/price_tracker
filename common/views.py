from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from alert.models import Alert, ArchiveAlert
from common.service import get_context_date_home


# Create your views here.

def custom_404(request: HttpRequest, exception):
    handler404 = custom_404
    return render(request, '404.html', status=404)


def home(request: HttpRequest) -> HttpResponse:

    context = get_context_date_home()

    return render(request, 'common/home_page.html', context)