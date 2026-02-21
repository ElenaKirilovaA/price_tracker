from django.urls import path

from alert import views

app_name = 'alert'

urlpatterns = [
        path('list/', views.display_active_alert, name='alert_list'),
        path('create/', views.alert_create, name='create'),
        path('<int:archived_id>/info/', views.archive_alert_info, name='info_archive'),
        path('<int:product_id>/check/', views.check_alerts, name='check'),
        path('<int:alert_id>/edit/', views.alert_edit, name='edit'),
        path('<int:alert_id>/delete/', views.alert_delete, name='delete'),
        path('past-alerts/', views.DisplayArchivedAlerts.as_view(), name='history_list')
    ]


