# webapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from .models import PrintJob, Department
from .forms import PrintJobForm

def home(request):
    # สถิติต่างๆ
    total_jobs = PrintJob.objects.count()
    pending_jobs = PrintJob.objects.filter(status='pending').count()
    printing_jobs = PrintJob.objects.filter(status='printing').count()
    completed_jobs = PrintJob.objects.filter(status='completed').count()
    
    # งานที่รอดำเนินการ (เรียงตามลำดับความสำคัญ)
    waiting_jobs = PrintJob.objects.filter(status='pending').order_by('-priority', 'date_needed')[:5]
    
    # งานที่เสร็จสิ้นล่าสุด
    recent_completed = PrintJob.objects.filter(status='completed').order_by('-date_completed')[:5]
    
    context = {
        'total_jobs': total_jobs,
        'pending_jobs': pending_jobs,
        'printing_jobs': printing_jobs,
        'completed_jobs': completed_jobs,
        'waiting_jobs': waiting_jobs,
        'recent_completed': recent_completed,
    }
    return render(request, 'webapp/home.html', context)

def job_list(request):
    jobs = PrintJob.objects.all().order_by('-priority', 'date_needed')
    return render(request, 'webapp/job_list.html', {'jobs': jobs})

def add_job(request):
    if request.method == 'POST':
        form = PrintJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()
            messages.success(request, f'เพิ่มงาน "{job.job_name}" เรียบร้อยแล้ว')
            return redirect('job_list')
    else:
        form = PrintJobForm()
    return render(request, 'webapp/add_job.html', {'form': form})

def job_detail(request, job_id):
    job = get_object_or_404(PrintJob, id=job_id)
    return render(request, 'webapp/job_detail.html', {'job': job})

def update_status(request, job_id):
    job = get_object_or_404(PrintJob, id=job_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        job.status = new_status
        
        if new_status == 'printing' and not job.date_started:
            job.date_started = timezone.now()
        elif new_status == 'completed' and not job.date_completed:
            job.date_completed = timezone.now()
            
        job.save()
        messages.success(request, f'อัปเดตสถานะงาน "{job.job_name}" เรียบร้อยแล้ว')
    
    return redirect('job_detail', job_id=job_id)