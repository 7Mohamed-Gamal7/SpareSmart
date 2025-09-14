from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('system-alerts/', views.system_alerts, name='system_alerts'),
    path('preferences/', views.user_preferences, name='preferences'),
    path('activity-log/', views.activity_log, name='activity_log'),
]