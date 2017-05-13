from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from core.models import Student, Teacher, Group, Enrolled, Teaches


def index(request):
    return HttpResponse('Royal Academy Of Programming - Visit Page')


def __divide_views(request, method_name, **kwargs):
    user = request.user
    if user.groups.filter(name='Student').exists():
        method_to_call = globals()['_' + method_name + '_student']
        if kwargs is not None:
            return method_to_call(request, **kwargs)
        else:
            return method_to_call(request)
    elif user.groups.filter(name='Teacher').exists():
        method_to_call = globals()['_' + method_name + '_teacher']
        if kwargs is not None:
            return method_to_call(request, **kwargs)
        else:
            return method_to_call(request)
    else:
        return HttpResponseForbidden()


@login_required()
def dashboard(request, **kwargs):
    return __divide_views(request, 'dashboard', **kwargs)


@login_required()
def group(request, **kwargs):
    return __divide_views(request, 'group', **kwargs) # TODO(aibeksmagulov): pass args to the method


def _group_student(request, pk, day=None):
    enrolled = get_object_or_404(Enrolled, student__user=request.user, group=pk)
    if enrolled.credits == 0:
        return HttpResponseForbidden() # TODO(aibeksmagulov): later add some customized page
    else:
        group = Group.objects.get(pk=pk)
        if day is None:
            day = group.day
        day = min(int(day), group.day)
        # TODO(aibeksmagulov): get slides and all other related info for a parameter day
        teachers = Teacher.objects.filter(teaches__group=pk)
        context = {'day': day, 'group': group, 'enrolled': enrolled, 'teachers': teachers}
        return render(request, 'student/group.html', context)


def _group_teacher(request, pk, day=None):
    teaches = get_object_or_404(Teaches, teacher__user=request.user, group=pk)
    group = Group.objects.get(pk=pk)
    if day is None:
        day = group.day
    day = min(int(day), group.day)
    # TODO(aibeksmagulov): get slides and all other related info for a parameter day
    students = Student.objects.filter(enrolled__group=pk)
    context = {'day': day, 'group': group, 'teaches': teaches, 'students': students}
    return render(request, 'teacher/group.html', context)


def _dashboard_student(request):
    enrolled_set = Enrolled.objects.filter(student__user=request.user)
    if enrolled_set is None:
        return HttpResponseForbidden() # TODO(aibeksmagulov): later add some customized page
    else:
        context = {'enrolled_set': enrolled_set}
        return render(request, 'student/dashboard.html', context)


def _dashboard_teacher(request):
    teaches_set = Teaches.objects.filter(teacher__user=request.user)
    context = {'teaches_set': teaches_set}
    return render(request, 'teacher/dashboard.html', context)