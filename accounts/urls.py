from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views
from accounts.views import AppUserDashboardView, AppUserProfileView, AppUserProfileEdit, AppUserProfileDelete

app_name = 'accounts'
urlpatterns = [
    path('', views.AppUserCreationView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(template_name='common/form_base.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', AppUserDashboardView.as_view(), name='dashboard'),

    path('profile/me/', AppUserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', AppUserProfileView.as_view(), name='profile-user'),

    path('profile/edit/', AppUserProfileEdit.as_view(), name='profile-edit'),
    path('profile/delete/me/', AppUserProfileDelete.as_view(), name='profile-delete'),
    path('profile/delete/<int:pk>/', AppUserProfileDelete.as_view(), name='profile-delete-manager'),
]