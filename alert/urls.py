from django.urls import path, include

from alert import views

app_name = 'alert'

paths = [
        path('info/', views.archive_alert_info, name='info_archive'),
        path('edit/', views.AlertEdit.as_view(), name='edit'),
        path('delete/', views.AlertDelete.as_view(), name='delete'),
]
urlpatterns = [
        path('list/', views.DisplayActiveAlerts.as_view(), name='alert_list'),
        path('create/', views.AlertCreate.as_view(), name='create'),
        path('<int:product_id>/check/', views.check_alerts, name='check'),

        path('<int:pk>/', include(paths)),
        path('past-alerts/', views.DisplayArchivedAlerts.as_view(), name='history_list')
    ]
