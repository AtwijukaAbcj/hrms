from django.test import TestCase
from .models import SapIntegrationConfig, SapSyncLog, SapEmployeeMapping
from employee.models import Employee, EmployeeTag
from django.contrib.auth.models import User


class SapIntegrationTestCase(TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = SapIntegrationConfig.objects.create(
            SAP_URL='https://test.sap.com/odata',
            SAP_USERNAME='testuser',
            SAP_PASSWORD='testpass',
            SAP_CLIENT='100',
            IS_ACTIVE=True
        )
        
        # Create test user and employee
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        
        self.employee = Employee.objects.create(
            employee_first_name='John',
            employee_last_name='Doe',
            email='john@example.com'
        )
    
    def test_sap_config_creation(self):
        """Test SAP configuration creation"""
        self.assertEqual(self.config.SAP_CLIENT, '100')
        self.assertTrue(self.config.IS_ACTIVE)
    
    def test_sap_sync_log_creation(self):
        """Test SAP sync log creation"""
        sync_log = SapSyncLog.objects.create(
            config=self.config,
            sync_type='employee',
            status='success',
            records_synced=5
        )
        self.assertEqual(sync_log.sync_type, 'employee')
        self.assertEqual(sync_log.status, 'success')
    
    def test_employee_mapping_creation(self):
        """Test employee SAP mapping"""
        mapping = SapEmployeeMapping.objects.create(
            solich_employee=self.employee,
            sap_employee_id='SAP12345'
        )
        self.assertEqual(mapping.sap_employee_id, 'SAP12345')
        self.assertFalse(mapping.is_synced)
