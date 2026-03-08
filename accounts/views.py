from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from accounts.forms import AppUserCreationForm
from alert.models import Alert
from product.models import Product

# Create your views here.

UserModel = get_user_model()

class AppUserCreationView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'common/form_base.html'
    success_url = reverse_lazy('common:home-page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'Create user'

        return context

    def post(self, request, *args, **kwargs):
        messages.success(request, f'Welcome {request.user}.')

        return redirect(self.success_url)


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{self.request.user}'s dashboard"
        context['products'] = Product.objects.filter(user=self.request.user)[:5]
        context['alerts'] = Alert.objects.filter(user=self.request.user)[:5]

        return context















