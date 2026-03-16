from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView

from accounts.forms import AppUserCreationForm, ProfileForm
from accounts.models import Profile
from alert.models import Alert, ArchiveAlert
from product.models import Product
from django.db.models import F, Sum, ExpressionWrapper, DecimalField

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
        context['archives'] = ArchiveAlert.objects.filter(user=self.request.user)[:5]


        return context

class AppUserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_page.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


    def get_context_data(self, **kwargs):

        archives = (
            ArchiveAlert.objects
            .filter(user=self.request.user)
            .aggregate(
                saved_money_db=Sum(
                    ExpressionWrapper(
                        F('started_price_eur') - F('triggered_price_eur'),
                        output_field=DecimalField()
                    )
                )
            )
        )
        context = super().get_context_data()
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
        context = super().get_context_data()
        context['page_title'] = 'Profile edit'

        return context

