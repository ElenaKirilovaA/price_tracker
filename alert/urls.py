from django.urls import path, include

from alert import views

app_name = 'alert'

paths = [
        path('info/', views.archive_alert_info, name='info_archive'),
        path('check/', views.check_alerts, name='check'),
        path('edit/', views.alert_edit, name='edit'),
        path('delete/', views.alert_delete, name='delete'),
]
urlpatterns = [
        path('list/', views.DisplayActiveAlerts.as_view(), name='alert_list'),
        path('create/', views.AlertCreate.as_view(), name='create'),
        path('<int:archived_id>/', include(paths)),
        path('past-alerts/', views.DisplayArchivedAlerts.as_view(), name='history_list')
    ]


