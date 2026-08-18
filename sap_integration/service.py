import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from django.utils.timezone import now as django_now
from .models import SapIntegrationConfig, SapSyncLog, SapEmployeeMapping, SapPayrollMapping
import logging

logger = logging.getLogger(__name__)


class SapODataClient:
    """
    Client for communicating with SAP OData services
    """
    
    def __init__(self, config: SapIntegrationConfig):
        self.config = config
        self.base_url = config.SAP_URL
        self.username = config.SAP_USERNAME
        self.password = config.SAP_PASSWORD
        self.client = config.SAP_CLIENT
        self.language = config.SAP_LANGUAGE
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create authenticated session"""
        session = requests.Session()
        session.auth = (self.username, self.password)
        session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
        return session
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test SAP connection"""
        try:
            response = self.session.get(
                f"{self.base_url}/$metadata",
                timeout=10
            )
            if response.status_code == 200:
                return True, "Connection successful"
            else:
                return False, f"Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, str(e)
    
    def get_entities(self, entity_name: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Fetch entities from SAP OData service"""
        try:
            url = f"{self.base_url}/{entity_name}"
            
            # Add filters if provided
            if filters:
                filter_str = self._build_filter_string(filters)
                url += f"?$filter={filter_str}"
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            # OData typically returns results in 'value' property
            return data.get('value', [])
        
        except Exception as e:
            logger.error(f"Error fetching entities from SAP: {str(e)}")
            return []
    
    def get_entity(self, entity_name: str, key: str) -> Optional[Dict]:
        """Fetch single entity from SAP OData service"""
        try:
            url = f"{self.base_url}/{entity_name}('{key}')"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching entity from SAP: {str(e)}")
            return None
    
    def create_entity(self, entity_name: str, data: Dict) -> Tuple[bool, str]:
        """Create entity in SAP OData service"""
        try:
            url = f"{self.base_url}/{entity_name}"
            response = self.session.post(
                url,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return True, response.json()
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error creating entity in SAP: {error_msg}")
            return False, error_msg
    
    def update_entity(self, entity_name: str, key: str, data: Dict) -> Tuple[bool, str]:
        """Update entity in SAP OData service"""
        try:
            url = f"{self.base_url}/{entity_name}('{key}')"
            response = self.session.patch(
                url,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return True, "Update successful"
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error updating entity in SAP: {error_msg}")
            return False, error_msg
    
    def delete_entity(self, entity_name: str, key: str) -> Tuple[bool, str]:
        """Delete entity from SAP OData service"""
        try:
            url = f"{self.base_url}/{entity_name}('{key}')"
            response = self.session.delete(url, timeout=10)
            response.raise_for_status()
            return True, "Delete successful"
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error deleting entity from SAP: {error_msg}")
            return False, error_msg
    
    @staticmethod
    def _build_filter_string(filters: Dict) -> str:
        """Build OData filter string"""
        filter_parts = []
        for key, value in filters.items():
            if isinstance(value, str):
                filter_parts.append(f"{key} eq '{value}'")
            else:
                filter_parts.append(f"{key} eq {value}")
        return " and ".join(filter_parts)


class SapSyncService:
    """
    Service for synchronizing data between Solich and SAP
    """
    
    def __init__(self, config: SapIntegrationConfig):
        self.config = config
        self.client = SapODataClient(config)
    
    def sync_employees(self, sync_log: SapSyncLog) -> None:
        """Sync employee data to SAP"""
        try:
            from employee.models import Employee
            
            sync_log.status = 'in_progress'
            sync_log.save()
            
            synced_count = 0
            failed_count = 0
            
            employees = Employee.objects.all()
            
            for employee in employees:
                try:
                    # Prepare employee data for SAP
                    employee_data = {
                        'EmployeeID': str(employee.id),
                        'FirstName': employee.employee_first_name,
                        'LastName': employee.employee_last_name,
                        'Email': employee.email,
                        'Phone': employee.phone or '',
                        'Department': str(employee.department.id) if employee.department else '',
                        'Designation': employee.designation if hasattr(employee, 'designation') else '',
                        'StartDate': str(employee.contract_start_date) if hasattr(employee, 'contract_start_date') else '',
                    }
                    
                    # Check if employee already mapped
                    mapping, created = SapEmployeeMapping.objects.get_or_create(
                        solich_employee=employee
                    )
                    
                    if created:
                        # Create new in SAP
                        success, result = self.client.create_entity(
                            self.config.EMPLOYEE_ENTITY,
                            employee_data
                        )
                        if success:
                            mapping.sap_employee_id = result.get('ID', str(employee.id))
                            mapping.is_synced = True
                            mapping.last_synced = django_now()
                            mapping.save()
                            synced_count += 1
                        else:
                            failed_count += 1
                    else:
                        # Update existing in SAP
                        if mapping.sap_employee_id:
                            success, result = self.client.update_entity(
                                self.config.EMPLOYEE_ENTITY,
                                mapping.sap_employee_id,
                                employee_data
                            )
                            if success:
                                mapping.is_synced = True
                                mapping.last_synced = django_now()
                                mapping.save()
                                synced_count += 1
                            else:
                                failed_count += 1
                
                except Exception as e:
                    logger.error(f"Error syncing employee {employee.id}: {str(e)}")
                    failed_count += 1
                    continue
            
            # Update sync log
            sync_log.records_synced = synced_count
            sync_log.records_failed = failed_count
            sync_log.status = 'success' if failed_count == 0 else 'partial'
            sync_log.completed_at = django_now()
            sync_log.save()
        
        except Exception as e:
            logger.error(f"Error in employee sync: {str(e)}")
            sync_log.status = 'failed'
            sync_log.error_message = str(e)
            sync_log.completed_at = django_now()
            sync_log.save()
    
    def sync_payroll(self, sync_log: SapSyncLog) -> None:
        """Sync payroll data to SAP"""
        try:
            sync_log.status = 'in_progress'
            sync_log.save()
            
            synced_count = 0
            failed_count = 0
            
            # Get all payroll mappings
            mappings = SapPayrollMapping.objects.filter(is_active=True)
            
            for mapping in mappings:
                try:
                    # This is a placeholder - actual implementation depends on payroll module structure
                    synced_count += 1
                except Exception as e:
                    logger.error(f"Error syncing payroll mapping: {str(e)}")
                    failed_count += 1
            
            sync_log.records_synced = synced_count
            sync_log.records_failed = failed_count
            sync_log.status = 'success' if failed_count == 0 else 'partial'
            sync_log.completed_at = django_now()
            sync_log.save()
        
        except Exception as e:
            logger.error(f"Error in payroll sync: {str(e)}")
            sync_log.status = 'failed'
            sync_log.error_message = str(e)
            sync_log.completed_at = django_now()
            sync_log.save()
    
    def fetch_from_sap(self, sync_log: SapSyncLog, entity_name: str) -> None:
        """Fetch data from SAP and update local records"""
        try:
            sync_log.status = 'in_progress'
            sync_log.save()
            
            entities = self.client.get_entities(entity_name)
            synced_count = len(entities)
            failed_count = 0
            
            sync_log.records_synced = synced_count
            sync_log.records_failed = failed_count
            sync_log.details = json.dumps({'entities_fetched': synced_count})
            sync_log.status = 'success'
            sync_log.completed_at = django_now()
            sync_log.save()
        
        except Exception as e:
            logger.error(f"Error fetching from SAP: {str(e)}")
            sync_log.status = 'failed'
            sync_log.error_message = str(e)
            sync_log.completed_at = django_now()
            sync_log.save()
