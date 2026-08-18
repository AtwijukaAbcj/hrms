# SAP Integration Module

This module enables seamless integration between Solich HRMS and SAP ERP systems through SAP's OData API.

## Features

- **Bi-directional Data Sync**: Synchronize employee, payroll, attendance, and leave data between Solich HRMS and SAP
- **Flexible Configuration**: Configure SAP connection details, sync intervals, and entity mappings through Django admin
- **Audit Trail**: Complete logging of all sync operations with success/failure tracking
- **Error Handling**: Comprehensive error logging and retry mechanisms
- **Manual & Automatic Sync**: Trigger syncs manually or enable automatic periodic synchronization
- **Data Mapping**: Define custom mappings between Solich and SAP data entities

## Installation

The module is already installed as part of Solich HRMS. To activate it:

1. **Add to INSTALLED_APPS** (already done):
   ```python
   INSTALLED_APPS = [
       ...
       'sap_integration',
       ...
   ]
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations sap_integration
   python manage.py migrate sap_integration
   ```

## Configuration

### Step 1: Access Django Admin

Navigate to `http://your-domain/admin/sap_integration/` to manage SAP integration settings.

### Step 2: Add SAP Configuration

1. Click "Add SAP Integration Config"
2. Enter your SAP connection details:
   - **SAP URL**: Base URL of your SAP OData service (e.g., `https://sap-server.example.com/odata/v4/`)
   - **SAP Username**: Your SAP username
   - **SAP Password**: Your SAP password
   - **SAP Client**: SAP client number (typically "100")
   - **SAP Language**: Language code (e.g., "EN" for English)

3. Configure sync settings:
   - **Auto Sync**: Enable automatic synchronization
   - **Sync Interval**: Time between syncs in seconds (default: 3600 = 1 hour)
   - **Employee Entity**: SAP OData entity name for employees (default: "Employees")

4. Save the configuration

### Step 3: Test Connection

Use the dashboard to test your SAP connection before enabling sync operations.

## Usage

### Dashboard

Access the SAP integration dashboard at: `/sap-integration/dashboard/`

Features:
- View current configuration status
- Display employee mapping statistics
- Show recent sync operations
- Quick actions for testing and triggering syncs

### Manual Synchronization

1. Go to the SAP Integration Dashboard
2. Click "Sync Employee Data"
3. Confirm the action
4. Monitor sync progress in the "Recent Sync Operations" table

### View Sync Logs

Navigate to `/sap-integration/sync-logs/` to view detailed logs of all sync operations:
- Sync type (employee, payroll, attendance, leave, recruitment, general)
- Status (success, failed, partial, in_progress)
- Number of records synced/failed
- Timestamps
- Error messages

## Data Models

### SapIntegrationConfig
Stores SAP connection configuration and sync settings.

**Fields**:
- `SAP_URL`: Base URL of SAP OData service
- `SAP_USERNAME`: SAP username
- `SAP_PASSWORD`: SAP password (encrypted)
- `SAP_CLIENT`: SAP client number
- `SAP_LANGUAGE`: Language code
- `AUTO_SYNC`: Enable automatic sync
- `SYNC_INTERVAL`: Time between syncs (seconds)
- `EMPLOYEE_ENTITY`: SAP entity name for employees
- `IS_ACTIVE`: Enable/disable integration
- `CREATED_AT`: Creation timestamp
- `UPDATED_AT`: Last update timestamp

### SapSyncLog
Audit trail for all sync operations.

**Fields**:
- `config`: Reference to SapIntegrationConfig
- `sync_type`: Type of sync (employee, payroll, attendance, leave, recruitment, general)
- `status`: Sync status (pending, in_progress, success, failed, partial)
- `records_synced`: Number of records successfully synced
- `records_failed`: Number of records that failed
- `started_at`: When sync started
- `completed_at`: When sync completed
- `error_message`: Error details if sync failed
- `details`: JSON field for additional details

### SapEmployeeMapping
Maps Solich employees to SAP employee IDs.

**Fields**:
- `solich_employee`: Reference to Employee
- `sap_employee_id`: SAP employee ID (unique)
- `sap_personnel_number`: SAP personnel number
- `is_synced`: Whether record is synced
- `last_synced`: Timestamp of last sync
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### SapPayrollMapping
Maps Solich payroll components to SAP wage types.

**Fields**:
- `solich_component`: Name of payroll component
- `sap_wage_type`: SAP wage type code
- `mapping_type`: Type of mapping (basic_salary, allowance, deduction, tax, contribution)
- `is_active`: Enable/disable mapping
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## API Endpoints

### Authentication

All API endpoints require Django authentication (login or token-based).

### Endpoints

- **GET** `/sap-integration/dashboard/` - View dashboard
- **GET/POST** `/sap-integration/configure/` - Configure SAP connection
- **POST** `/sap-integration/test-connection/` - Test SAP connection
- **POST** `/sap-integration/sync-employees/` - Trigger employee sync
- **GET** `/sap-integration/sync-logs/` - View sync logs

## Development

### Service Classes

The module provides service classes for SAP integration:

#### SapODataClient
Handles low-level communication with SAP OData API.

```python
from sap_integration.service import SapODataClient
from sap_integration.models import SapIntegrationConfig

config = SapIntegrationConfig.objects.first()
client = SapODataClient(config)

# Test connection
success, message = client.test_connection()

# Fetch entities
employees = client.get_entities('Employees')

# Get single entity
employee = client.get_entity('Employees', 'EMP001')

# Create entity
success, result = client.create_entity('Employees', {
    'EmployeeID': 'EMP123',
    'FirstName': 'John',
    'LastName': 'Doe'
})
```

#### SapSyncService
Handles business logic for synchronizing Solich and SAP data.

```python
from sap_integration.service import SapSyncService
from sap_integration.models import SapIntegrationConfig, SapSyncLog

config = SapIntegrationConfig.objects.first()
service = SapSyncService(config)

# Create sync log
sync_log = SapSyncLog.objects.create(
    config=config,
    sync_type='employee',
    status='pending'
)

# Sync employees
service.sync_employees(sync_log)

# Sync payroll
service.sync_payroll(sync_log)
```

## Troubleshooting

### Connection Fails
1. Verify SAP URL is correct and accessible
2. Check SAP username/password are correct
3. Verify SAP client number
4. Check network connectivity to SAP server
5. Ensure SAP OData service is enabled

### Sync Failures
1. Check sync logs for detailed error messages
2. Verify employee data in Solich has required fields
3. Check SAP wage type codes in payroll mappings
4. Review employee mappings in Django admin

### Performance Issues
1. Increase `SYNC_INTERVAL` to reduce frequency
2. Limit number of records in single sync
3. Consider implementing batch processing
4. Monitor database performance

## Security Considerations

- **Credentials**: SAP passwords are stored encrypted in the database
- **Authentication**: All API endpoints require login
- **Audit Trail**: All sync operations are logged
- **SSL/TLS**: Ensure SAP connection uses HTTPS
- **Data Privacy**: Configure appropriate employee data access permissions

## Support & Contributions

For issues or feature requests, please contact the development team.

## License

This module is part of Solich HRMS and follows the same license terms.
