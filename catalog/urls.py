from django.urls import path, include
from catalog import views

app_name = 'catalog'

tag_urls = [
    path('create/', views.bulk_create_tags, name='tag_create'),
    path('display/', views.tag_display, name='display'),
    path('delete/', views.tag_bulk_delete, name='delete_tag')
]

category_id_urls = [
    path('info/', views.category_info, name='info'),

    path('edit/', views.edit_category, name='edit'),
    path('delete/', views.delete_category, name='delete'),
]
urlpatterns  = [
    path('', views.catalog_overview, name='catalog-overview'),


    path('create/', views.add_category, name='create'),
    path('<int:category_id>/', include(category_id_urls)),

    path('tag/', include(tag_urls)),
]


