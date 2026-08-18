from django import forms
from .models import SapIntegrationConfig, SapPayrollMapping


class SapIntegrationConfigForm(forms.ModelForm):
    SAP_PASSWORD = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = SapIntegrationConfig
        fields = [
            'SAP_URL',
            'SAP_USERNAME',
            'SAP_PASSWORD',
            'SAP_CLIENT',
            'SAP_LANGUAGE',
            'AUTO_SYNC',
            'SYNC_INTERVAL',
            'EMPLOYEE_ENTITY',
            'IS_ACTIVE'
        ]
        widgets = {
            'SAP_URL': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://sap-server.example.com/odata/v4/'
            }),
            'SAP_USERNAME': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SAP Username'
            }),
            'SAP_PASSWORD': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'SAP Password'
            }),
            'SAP_CLIENT': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '100'
            }),
            'SAP_LANGUAGE': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'EN'
            }),
            'SYNC_INTERVAL': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seconds'
            }),
            'EMPLOYEE_ENTITY': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Employees'
            }),
            'AUTO_SYNC': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'IS_ACTIVE': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class SapPayrollMappingForm(forms.ModelForm):
    class Meta:
        model = SapPayrollMapping
        fields = ['solich_component', 'sap_wage_type', 'mapping_type', 'is_active']
        widgets = {
            'solich_component': forms.TextInput(attrs={'class': 'form-control'}),
            'sap_wage_type': forms.TextInput(attrs={'class': 'form-control'}),
            'mapping_type': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
