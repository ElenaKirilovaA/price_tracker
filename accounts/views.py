from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, DeleteView
from accounts.forms import AppUserCreationForm, ProfileForm
from accounts.models import Profile
from alert.models import Alert, ArchiveAlert
from common.mixins import AppUserQuerysetMixin, PageTitleMixin
from price_tracker import settings
from product.models import Product
from django.db.models import F, Sum, ExpressionWrapper, DecimalField, Count

# Create your views here.

UserModel = get_user_model()

class AppUserCreationView(PageTitleMixin, CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'common/form_base.html'
    success_url = reverse_lazy('accounts:profile')
    page_title = 'Create user'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.object)
        messages.success(self.request, f'Welcome {self.object.get_username()}.')

        return response

class AppUserDashboardView(LoginRequiredMixin, PageTitleMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_page_title(self):
        return f"{self.request.user}'s dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(user=self.request.user)[:5]
        context['favourite_products'] = self.request.user.favourite_product.all()[:5]
        context['alerts'] = Alert.objects.filter(user=self.request.user)[:5]
        context['archives'] = ArchiveAlert.objects.filter(user=self.request.user)[:5]

        return context

class AppUserProfileView(LoginRequiredMixin, UserPassesTestMixin ,DetailView):
    model = Profile
    template_name = 'accounts/profile_page.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk:
           return Profile.objects.get(pk=pk)

        return self.request.user.profile

    def test_func(self):
        user = self.request.user
        profile = self.get_object()

        return user == profile.user or user.has_perm('accounts.view_profile')


    def get_context_data(self, **kwargs):
        profile = self.get_object()
        archives = (
            ArchiveAlert.objects
            .filter(user=profile.user)
            .aggregate(saved_money_db=Sum(ExpressionWrapper(F('started_price_eur') - F('triggered_price_eur'),output_field=DecimalField()))))
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Profile'
        context['money_saved'] = archives['saved_money_db'] or 0

        return context

class AppUserProfileEdit(LoginRequiredMixin, PageTitleMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'common/form_base.html'
    success_url = reverse_lazy('accounts:profile')
    page_title = 'Profile edit'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


class AppUserProfileDelete(LoginRequiredMixin, UserPassesTestMixin, PageTitleMixin, DeleteView):
    model = UserModel
    template_name = 'common/form_delete_category.html'
    success_url = reverse_lazy('common:home-page')
    page_title = 'Delete profile'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk:
            return UserModel.objects.get(pk=pk)

        return self.request.user

    def test_func(self):
        user = self.request.user
        other_user = self.get_object()
        return user == other_user or user.has_perm('accounts.delete_appuser')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()

        if user == request.user:
            logout(request)

        return super().delete(request, *args, **kwargs)


class AppUserChangePassword(PageTitleMixin, PasswordChangeView):
    template_name = 'common/form_base.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your password has been changed')

        return response


class AppUserPasswordReset(PageTitleMixin, PasswordResetView):
    template_name = 'common/form_base.html'
    email_template_name = 'accounts/password-template.txt'
    subject_template_name = 'accounts/account-password-subject.txt'
    from_email = settings.DEFAULT_FROM_EMAIL
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'We’ve sent you an email with instructions to reset your password.')

        return response


