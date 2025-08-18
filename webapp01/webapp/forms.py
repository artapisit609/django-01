# webapp/forms.py
from django import forms
from .models import PrintJob, Department

class PrintJobForm(forms.ModelForm):
    class Meta:
        model = PrintJob
        fields = [
            'job_name', 'description', 'department', 'requestor',
            'date_needed', 'priority', 'print_time_hours', 
            'material_weight_grams', 'material_type', 'file_upload'
        ]
        widgets = {
            'job_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'requestor': forms.TextInput(attrs={'class': 'form-control'}),
            'date_needed': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'print_time_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'material_weight_grams': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'material_type': forms.TextInput(attrs={'class': 'form-control'}),
            'file_upload': forms.FileInput(attrs={'class': 'form-control'}),
        }