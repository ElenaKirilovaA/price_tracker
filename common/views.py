from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.

def custom_404(request: HttpRequest, exception):
    handler404 = custom_404
    return render(request, '404.html', status=404)