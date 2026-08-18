from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import SapIntegrationConfig, SapSyncLog, SapEmployeeMapping
from .forms import SapIntegrationConfigForm
import requests
from datetime import datetime
import json


@login_required
def sap_integration_dashboard(request):
    """
    Dashboard for SAP integration status and management
    """
    try:
        config = SapIntegrationConfig.objects.first()
    except SapIntegrationConfig.DoesNotExist:
        config = None
    
    recent_syncs = SapSyncLog.objects.all()[:10]
    mapped_employees = SapEmployeeMapping.objects.filter(is_synced=True).count()
    total_employees = SapEmployeeMapping.objects.count()
    
    context = {
        'config': config,
        'recent_syncs': recent_syncs,
        'mapped_employees': mapped_employees,
        'total_employees': total_employees,
    }
    return render(request, 'sap_integration/dashboard.html', context)


@login_required
def configure_sap(request):
    """
    Configure SAP integration settings
    """
    config = SapIntegrationConfig.objects.first()
    
    if request.method == 'POST':
        form = SapIntegrationConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'SAP configuration updated successfully')
            return redirect('sap_integration_dashboard')
    else:
        form = SapIntegrationConfigForm(instance=config)
    
    context = {'form': form}
    return render(request, 'sap_integration/configure.html', context)


@login_required
@require_POST
def test_sap_connection(request):
    """
    Test SAP connection
    """
    try:
        config = SapIntegrationConfig.objects.first()
        if not config:
            return JsonResponse({
                'status': 'error',
                'message': 'SAP configuration not found'
            })
        
        # Test basic connectivity
        try:
            response = requests.get(
                f"{config.SAP_URL}/$metadata",
                auth=(config.SAP_USERNAME, config.SAP_PASSWORD),
                timeout=10
            )
            
            if response.status_code == 200:
                return JsonResponse({
                    'status': 'success',
                    'message': 'SAP connection successful'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Connection failed with status {response.status_code}'
                })
        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Connection error: {str(e)}'
            })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })


@login_required
@require_POST
def sync_employee_data(request):
    """
    Trigger manual sync of employee data to SAP
    """
    try:
        config = SapIntegrationConfig.objects.first()
        if not config:
            return JsonResponse({
                'status': 'error',
                'message': 'SAP configuration not found'
            })
        
        # Create sync log entry
        sync_log = SapSyncLog.objects.create(
            config=config,
            sync_type='employee',
            status='in_progress'
        )
        
        # Get all mapped employees
        from employee.models import Employee
        employees = Employee.objects.all()
        
        synced_count = 0
        failed_count = 0
        
        for employee in employees:
            try:
                # Prepare employee data
                employee_data = {
                    'EmployeeID': str(employee.id),
                    'FirstName': employee.employee_first_name,
                    'LastName': employee.employee_last_name,
                    'Email': employee.email,
                    'Department': str(employee.department.id) if employee.department else '',
                }
                
                # Send to SAP (placeholder - actual implementation depends on SAP API)
                # For now, just create/update mapping
                mapping, created = SapEmployeeMapping.objects.get_or_create(
                    solich_employee=employee,
                    defaults={'sap_employee_id': str(employee.id)}
                )
                mapping.is_synced = True
                mapping.last_synced = datetime.now()
                mapping.save()
                
                synced_count += 1
                
            except Exception as e:
                failed_count += 1
                continue
        
        # Update sync log
        sync_log.records_synced = synced_count
        sync_log.records_failed = failed_count
        sync_log.status = 'success' if failed_count == 0 else 'partial'
        sync_log.completed_at = datetime.now()
        sync_log.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Sync completed: {synced_count} employees synced, {failed_count} failed',
            'records_synced': synced_count,
            'records_failed': failed_count
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Sync error: {str(e)}'
        })


@login_required
def view_sync_logs(request):
    """
    View all SAP sync logs
    """
    logs = SapSyncLog.objects.all().order_by('-started_at')
    
    # Filter by sync type
    sync_type = request.GET.get('sync_type')
    if sync_type:
        logs = logs.filter(sync_type=sync_type)
    
    context = {
        'logs': logs,
        'sync_type': sync_type
    }
    return render(request, 'sap_integration/sync_logs.html', context)
