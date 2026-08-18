from django.contrib import admin
from .models import (
    SapIntegrationConfig,
    SapSyncLog,
    SapEmployeeMapping,
    SapPayrollMapping
)


@admin.register(SapIntegrationConfig)
class SapIntegrationConfigAdmin(admin.ModelAdmin):
    list_display = ['SAP_CLIENT', 'SAP_URL', 'IS_ACTIVE', 'AUTO_SYNC', 'UPDATED_AT']
    list_filter = ['IS_ACTIVE', 'AUTO_SYNC', 'UPDATED_AT']
    readonly_fields = ['CREATED_AT', 'UPDATED_AT']
    
    fieldsets = (
        ('SAP Connection', {
            'fields': ('SAP_URL', 'SAP_USERNAME', 'SAP_PASSWORD', 'SAP_CLIENT', 'SAP_LANGUAGE')
        }),
        ('Sync Configuration', {
            'fields': ('AUTO_SYNC', 'SYNC_INTERVAL', 'EMPLOYEE_ENTITY')
        }),
        ('Status', {
            'fields': ('IS_ACTIVE', 'CREATED_AT', 'UPDATED_AT')
        }),
    )


@admin.register(SapSyncLog)
class SapSyncLogAdmin(admin.ModelAdmin):
    list_display = ['sync_type', 'status', 'records_synced', 'records_failed', 'started_at', 'completed_at']
    list_filter = ['sync_type', 'status', 'started_at']
    search_fields = ['error_message']
    readonly_fields = ['started_at', 'completed_at']
    
    fieldsets = (
        ('Sync Information', {
            'fields': ('config', 'sync_type', 'status')
        }),
        ('Results', {
            'fields': ('records_synced', 'records_failed', 'error_message')
        }),
        ('Timeline', {
            'fields': ('started_at', 'completed_at')
        }),
        ('Details', {
            'fields': ('details',)
        }),
    )


@admin.register(SapEmployeeMapping)
class SapEmployeeMappingAdmin(admin.ModelAdmin):
    list_display = ['solich_employee', 'sap_employee_id', 'is_synced', 'last_synced']
    list_filter = ['is_synced', 'last_synced']
    search_fields = ['sap_employee_id', 'solich_employee__employee_first_name']
    readonly_fields = ['created_at', 'updated_at', 'last_synced']


@admin.register(SapPayrollMapping)
class SapPayrollMappingAdmin(admin.ModelAdmin):
    list_display = ['solich_component', 'sap_wage_type', 'mapping_type', 'is_active']
    list_filter = ['mapping_type', 'is_active']
    search_fields = ['solich_component', 'sap_wage_type']
