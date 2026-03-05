from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', views.AppUserCreationView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(template_name='common/form_base.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]