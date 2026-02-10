from django.urls import path, include

from alert import views

app_name = 'alert'
urlpatterns = [
    path('', views.home, name='home-page'),
    path('alert/', include([
        path('', views.display_active_alert, name='alert_list'),

        path('create/', views.alert_create, name='create'),
        path('<int:archived_id>/info/', views.archive_alert_info, name='info_archive'),
        path('<int:product_id>/check/', views.check_alerts, name='check'),
        path('<int:alert_id>/edit/', views.alert_edit, name='edit'),
        path('<int:alert_id>/delete/', views.alert_delete, name='delete'),
        path('past-alerts', views.display_archived_alert, name='history_list')
    ]))


]