from django.urls import path, include

from product import views

app_name = 'product'

paths = [
        path('edit/', views.EditProduct.as_view(), name='edit'),
        path('delete/', views.DeleteProduct.as_view(), name='delete'),
        path('info/', views.SingleProduct.as_view(), name='single_product'),
        path('like/', views.liked_product, name='liked_product'),
    ]

urlpatterns = [
    path('', views.ProductList.as_view(), name='list'),

    path('user/', views.AppUserProductList.as_view(), name='product_list'),
    path('user/favourites/', views.AppUserFavouriteProductList.as_view(), name='product_favourite_list'),
    path('create/', views.AddProduct.as_view(), name='create'),
    path('<slug:slug>/', include(paths)),
]
