# webapp/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่อแผนก")
    code = models.CharField(max_length=10, unique=True, verbose_name="รหัสแผนก")
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        verbose_name = "แผนก"
        verbose_name_plural = "แผนก"

class PrintJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอดำเนินการ'),
        ('printing', 'กำลังพิมพ์'),
        ('completed', 'เสร็จสิ้น'),
        ('cancelled', 'ยกเลิก'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'ต่ำ'),
        ('normal', 'ปกติ'),
        ('high', 'สูง'),
        ('urgent', 'เร่งด่วน'),
    ]
    
    # ข้อมูลงาน
    job_name = models.CharField(max_length=200, verbose_name="ชื่องาน")
    description = models.TextField(blank=True, verbose_name="รายละเอียด")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="แผนก")
    requestor = models.CharField(max_length=100, verbose_name="ผู้ขอ")
    
    # วันที่
    date_requested = models.DateTimeField(default=timezone.now, verbose_name="วันที่ขอ")
    date_needed = models.DateField(verbose_name="วันที่ต้องการ")
    date_started = models.DateTimeField(null=True, blank=True, verbose_name="วันที่เริ่มพิมพ์")
    date_completed = models.DateTimeField(null=True, blank=True, verbose_name="วันที่เสร็จสิ้น")
    
    # สถานะและลำดับความสำคัญ
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="สถานะ")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal', verbose_name="ลำดับความสำคัญ")
    
    # ข้อมูลการพิมพ์
    print_time_hours = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="เวลาพิมพ์ (ชั่วโมง)")
    material_weight_grams = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="น้ำหนักวัสดุ (กรัม)")
    material_type = models.CharField(max_length=50, default="PLA", verbose_name="ชนิดวัสดุ")
    
    # ต้นทุน
    material_cost_per_gram = models.DecimalField(max_digits=6, decimal_places=2, default=0.50, verbose_name="ราคาวัสดุต่อกรัม")
    electricity_cost_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=5.00, verbose_name="ค่าไฟต่อชั่วโมง")
    labor_cost_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=50.00, verbose_name="ค่าแรงต่อชั่วโมง")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="ต้นทุนรวม")
    
    # ไฟล์งาน
    file_upload = models.FileField(upload_to='print_jobs/', null=True, blank=True, verbose_name="ไฟล์ STL/3MF")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # เพิ่ม methods สำหรับคำนวณต้นทุน
    @property
    def material_cost(self):
        """คำนวณค่าวัสดุ"""
        if self.material_weight_grams and self.material_cost_per_gram:
            return float(self.material_weight_grams) * float(self.material_cost_per_gram)
        return 0
    
    @property
    def electricity_cost(self):
        """คำนวณค่าไฟ"""
        if self.print_time_hours and self.electricity_cost_per_hour:
            return float(self.print_time_hours) * float(self.electricity_cost_per_hour)
        return 0
    
    @property
    def labor_cost(self):
        """คำนวณค่าแรง"""
        if self.print_time_hours and self.labor_cost_per_hour:
            return float(self.print_time_hours) * float(self.labor_cost_per_hour)
        return 0
    
    def save(self, *args, **kwargs):
        # คำนวณต้นทุนอัตโนมัติ
        if self.print_time_hours and self.material_weight_grams:
            self.total_cost = self.material_cost + self.electricity_cost + self.labor_cost
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.job_name} - {self.department.code}"
    
    class Meta:
        verbose_name = "งานพิมพ์ 3D"
        verbose_name_plural = "งานพิมพ์ 3D"
        ordering = ['-priority', 'date_needed', 'date_requested']