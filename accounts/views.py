from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView

from accounts.forms import AppUserCreationForm, ProfileForm
from accounts.models import Profile
from alert.models import Alert
from common.mixins import AppUserQuerysetMixin
from product.models import Product

# Create your views here.

UserModel = get_user_model()

class AppUserCreationView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'common/form_base.html'
    success_url = reverse_lazy('accounts:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create user'

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'Welcome {self.object.get_username()}.' )
        return response


class AppUserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{self.request.user}'s dashboard"
        context['products'] = Product.objects.filter(user=self.request.user)[:5]
        context['alerts'] = Alert.objects.filter(user=self.request.user)[:5]

        return context

class AppUserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_page.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Profile'

        return context

    def get_object(self, queryset=None):
        return self.request.user.profile


class AppUserProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'common/form_base.html'
    success_url = reverse_lazy('accounts:profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = f'Update {str(self)} info'

        return context
