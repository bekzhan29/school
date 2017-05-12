from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse('Royal Academy Of Programming - Visit Page')

@login_required()
def dashboard(request):
    # TODO(aibeksmagulov): Add separation for student and teacher dashboards

    return _dashboard_student(request)

def _dashboard_student(request):
    return render(request, 'student/dashboard.html')

def _dashboard_teacher(request):
    return render(request, 'teacher/dashboard.html')