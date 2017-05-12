from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse('Royal Academy Of Programming - Visit Page')

@login_required()
def dashboard(request):
    # TODO(aibeksmagulov): Add separation for student and teacher dashboards
    user = request.user
    if user.groups.filter(name='Student').exists():
        return _dashboard_student(request)
    elif user.groups.filter(name='Teacher').exists():
        return _dashboard_teacher(request)
    else:
        return HttpResponseForbidden()

def _dashboard_student(request):
    return render(request, 'student/dashboard.html')

def _dashboard_teacher(request):
    return render(request, 'teacher/dashboard.html')