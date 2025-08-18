from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("<h1>Hello from Engineer!</h1><p>This is my first home page</p>")

def about(request):
    context = {
        'title': 'About Team',
        'message': 'Welcome to Engineer'
    }
    return HttpResponse(f"<h1>{context['title']}</h1><p>{context['message']}</p>")