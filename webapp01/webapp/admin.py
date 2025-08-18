# webapp/admin.py
from django.contrib import admin
from .models import Department, PrintJob

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']
    list_filter = ['code']

@admin.register(PrintJob)
class PrintJobAdmin(admin.ModelAdmin):
    list_display = [
        'job_name', 'department', 'requestor', 'status', 
        'priority', 'date_needed', 'total_cost'
    ]
    list_filter = [
        'status', 'priority', 'department', 'material_type',
        'date_requested', 'date_needed'
    ]
    search_fields = ['job_name', 'requestor', 'description']
    readonly_fields = ['total_cost', 'created_at', 'updated_at']
    
    fieldsets = (
        ('ข้อมูลงาน', {
            'fields': ('job_name', 'description', 'department', 'requestor')
        }),
        ('ลำดับความสำคัญและสถานะ', {
            'fields': ('priority', 'status')
        }),
        ('วันที่', {
            'fields': ('date_needed', 'date_started', 'date_completed')
        }),
        ('ข้อมูลการพิมพ์', {
            'fields': ('print_time_hours', 'material_weight_grams', 'material_type', 'file_upload')
        }),
        ('ต้นทุน', {
            'fields': (
                'material_cost_per_gram', 'electricity_cost_per_hour', 
                'labor_cost_per_hour', 'total_cost'
            )
        }),
        ('ข้อมูลระบบ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # แสดงข้อมูลเพิ่มเติมในหน้ารายการ
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('department')