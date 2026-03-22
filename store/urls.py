from django.urls import path

from store import views

app_name = 'store'
urlpatterns = [
    path('', views.StorePageView.as_view(), name='main'),

    path('api/', views.ListStoreView.as_view(), name='list'),
    path('api/<int:pk>/', views.DetailStoreView.as_view(), name='detail'),
]