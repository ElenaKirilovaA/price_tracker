from django.urls import path, include
from catalog import views

app_name = 'catalog'

tag_urls = [
    path('create/', views.bulk_create_tags, name='tag_create'),
    path('display/', views.tag_display, name='display'),
    path('delete/', views.tag_bulk_delete, name='delete_tag')
]

category_id_urls = [
    path('info/', views.CategoryInfo.as_view(), name='info'),

    path('edit/', views.EditCategory.as_view(), name='edit'),
    path('delete/', views.DeleteCategory.as_view(), name='delete'),
]
urlpatterns  = [
    path('', views.CatalogOverview.as_view(), name='catalog-overview'),


    path('create/', views.AddCategory.as_view(), name='create'),
    path('<int:pk>/', include(category_id_urls)),

    path('tag/', include(tag_urls)),
]


