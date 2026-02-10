from django.urls import path, include

from product import views

app_name = 'product'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.add_product, name='create'),
    path('<slug:slug>/edit/', views.edit_product, name='edit'),
    path('<slug:slug>/delete/', views.delete_product, name='delete'),
    path('<slug:slug>/info/', views.single_product, name='single_product'),
]