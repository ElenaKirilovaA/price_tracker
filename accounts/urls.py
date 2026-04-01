from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from accounts import views
from accounts.views import AppUserDashboardView, AppUserProfileView, AppUserProfileEdit, AppUserProfileDelete

app_name = 'accounts'
urlpatterns = [
    path('', views.AppUserCreationView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', views.AppUserChangePassword.as_view(), name='password_change'),
    path('password-reset/', views.AppUserPasswordReset.as_view(),  name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='common/form_base.html'),  name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(
        template_name='accounts/password-reset-confirm.html',
        success_url=reverse_lazy('accounts:login')),  name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='accounts/password-reset-complete.html'
    ), name='password_reset_complete'),
    path('dashboard/', AppUserDashboardView.as_view(), name='dashboard'),

    path('profile/me/', AppUserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', AppUserProfileView.as_view(), name='profile-user'),

    path('profile/edit/', AppUserProfileEdit.as_view(), name='profile-edit'),
    path('profile/delete/me/', AppUserProfileDelete.as_view(), name='profile-delete'),
    path('profile/delete/<int:pk>/', AppUserProfileDelete.as_view(), name='profile-delete-manager'),

]