from django.urls import path
from . import views

app_name = 'sap_integration'

urlpatterns = [
    path('dashboard/', views.sap_integration_dashboard, name='dashboard'),
    path('configure/', views.configure_sap, name='configure'),
    path('test-connection/', views.test_sap_connection, name='test_connection'),
    path('sync-employees/', views.sync_employee_data, name='sync_employees'),
    path('sync-logs/', views.view_sync_logs, name='sync_logs'),
]
