from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView

from common.service import get_context_date_home, get_context_date_moderator_home


# Create your views here.

def custom_404(request: HttpRequest, exception):
    return render(request, '404.html', status=404)


class HomeView(TemplateView):

    def get_template_names(self):
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Moderator').exists():
            return ['common/home_moderator.html']
        return ['common/home_page.html']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Moderator').exists():
            context.update(get_context_date_moderator_home())
        else:
            context.update(get_context_date_home())
        return context
