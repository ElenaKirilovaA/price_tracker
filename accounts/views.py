from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import AppUserCreationForm

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
