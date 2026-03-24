from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, DeleteView
from accounts.forms import AppUserCreationForm, ProfileForm
from accounts.models import Profile
from alert.models import Alert, ArchiveAlert
from common.mixins import AppUserQuerysetMixin
from product.models import Product
from django.db.models import F, Sum, ExpressionWrapper, DecimalField, Count

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

class AppUserDashboardView(LoginRequiredMixin,  TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{self.request.user}'s dashboard"
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
        print(profile)

        archives = (
            ArchiveAlert.objects
            .filter(user=profile.user)
            .aggregate(
                saved_money_db=Sum(
                    ExpressionWrapper(
                        F('started_price_eur') - F('triggered_price_eur'),
                        output_field=DecimalField()
                    )
                )
            )
        )
        context = super().get_context_data(**kwargs)
        context['money_saved'] = archives['saved_money_db'] or 0
        return context

class AppUserProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'common/form_base.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Profile edit'

        return context

class AppUserProfileDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserModel
    template_name = 'common/form_delete_category.html'
    success_url = reverse_lazy('common:home-page')

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

