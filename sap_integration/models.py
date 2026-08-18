from django.db import models
from django.core.validators import URLValidator
from employee.models import Employee
from django.utils.translation import gettext_lazy as _


class SapIntegrationConfig(models.Model):
    """
    Model to store SAP integration configuration
    """
    SAP_URL = models.CharField(
        max_length=500,
        help_text="SAP OData service URL",
        validators=[URLValidator()]
    )
    SAP_USERNAME = models.CharField(max_length=255, blank=True)
    SAP_PASSWORD = models.CharField(max_length=500, blank=True)
    SAP_CLIENT = models.CharField(max_length=10, default="100")
    SAP_LANGUAGE = models.CharField(max_length=2, default="EN")
    
    # Sync settings
    AUTO_SYNC = models.BooleanField(default=True)
    SYNC_INTERVAL = models.IntegerField(default=3600, help_text="Sync interval in seconds")
    
    # Entity mappings
    EMPLOYEE_ENTITY = models.CharField(
        max_length=255,
        default="Employees",
        help_text="SAP entity name for employees"
    )
    
    IS_ACTIVE = models.BooleanField(default=True)
    CREATED_AT = models.DateTimeField(auto_now_add=True)
    UPDATED_AT = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("SAP Integration Configuration")
        verbose_name_plural = _("SAP Integration Configurations")
    
    def __str__(self):
        return f"SAP Integration - {self.SAP_CLIENT}"


class SapSyncLog(models.Model):
    """
    Model to track SAP sync history
    """
    SYNC_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('success', _('Success')),
        ('failed', _('Failed')),
        ('partial', _('Partial Success')),
    ]
    
    SYNC_TYPE_CHOICES = [
        ('employee', _('Employee')),
        ('payroll', _('Payroll')),
        ('attendance', _('Attendance')),
        ('leave', _('Leave')),
        ('recruitment', _('Recruitment')),
        ('general', _('General')),
    ]
    
    config = models.ForeignKey(
        SapIntegrationConfig,
        on_delete=models.CASCADE,
        related_name='sync_logs'
    )
    sync_type = models.CharField(max_length=50, choices=SYNC_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=SYNC_STATUS_CHOICES, default='pending')
    
    records_synced = models.IntegerField(default=0)
    records_failed = models.IntegerField(default=0)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    error_message = models.TextField(blank=True)
    details = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = _("SAP Sync Log")
        verbose_name_plural = _("SAP Sync Logs")
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.sync_type} - {self.status} ({self.started_at})"


class SapEmployeeMapping(models.Model):
    """
    Model to map Solich employees to SAP employees
    """
    solich_employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='sap_mapping'
    )
    sap_employee_id = models.CharField(max_length=255, unique=True)
    sap_personnel_number = models.CharField(max_length=255, blank=True)
    
    is_synced = models.BooleanField(default=False)
    last_synced = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("SAP Employee Mapping")
        verbose_name_plural = _("SAP Employee Mappings")
    
    def __str__(self):
        return f"{self.solich_employee.employee_first_name} - {self.sap_employee_id}"


class SapPayrollMapping(models.Model):
    """
    Model to map payroll components between Solich and SAP
    """
    MAPPING_TYPE_CHOICES = [
        ('basic_salary', _('Basic Salary')),
        ('allowance', _('Allowance')),
        ('deduction', _('Deduction')),
        ('tax', _('Tax')),
        ('contribution', _('Contribution')),
    ]
    
    solich_component = models.CharField(max_length=255)
    sap_wage_type = models.CharField(max_length=10)  # SAP wage type code
    mapping_type = models.CharField(max_length=50, choices=MAPPING_TYPE_CHOICES)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("SAP Payroll Mapping")
        verbose_name_plural = _("SAP Payroll Mappings")
        unique_together = ('solich_component', 'sap_wage_type')
    
    def __str__(self):
        return f"{self.solich_component} -> {self.sap_wage_type}"
