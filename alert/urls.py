from django.urls import path, include

from alert import views

app_name = 'alert'

paths = [
        path('info/', views.ArchiveAlertInfo.as_view(), name='info_archive'),
        path('edit/', views.AlertEdit.as_view(), name='edit'),
        path('delete/', views.AlertDelete.as_view(), name='delete'),
]
urlpatterns = [
        path('list/', views.DisplayActiveAlerts.as_view(), name='alert_list'),
        path('list/user/', views.DisplayAppUserActiveAlerts.as_view(), name='user-alert_list'),
        path('create/', views.AlertCreate.as_view(), name='create'),
        path('<int:pk>/', include(paths)),
        path('past-alerts/', views.DisplayArchivedAlerts.as_view(), name='history_list'),
        path('user-past-alerts/', views.DisplayAppUserArchiveAlert.as_view(), name='user-history_list'),
    ]
