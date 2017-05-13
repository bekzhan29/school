from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from core.models import Student, Teacher, Group, Enrolled, Teaches, Section, TeacherAttendance, \
    StudentAttendance
import datetime
from django.db.models import F


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


@login_required()
def attend(request, **kwargs):
    return __divide_views(request, 'attend', **kwargs)


# TODO(aibeksmagulov): just for now, only those teachers can check their attendances who are in a
# right section and current time is within the allowed time given for attendance check.
# In case if an assigned teacher doesn't show up, we allow an administrator to assign a new teacher
# to the group and add him to that section just for once. Maybe we can add an expiration_date
# field to the Section model? So, then the new teacher can check his attendance. In extreme cases,
# when there is not any available teacher, we will put video lectures and check teacher attendance,
# by ourselves. Or administrator can do the same. Maybe administrator can check the lesson, too?
# Or maybe an administrator can have an attendance form where he can check the attendance and
# assign a new teacher if needed.
def _attend_teacher(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes=20)
    try:
        # BUG: if starting time of a lesson is 23:50 than it will not find what it should
        # TODO(aibeksmagulov): change the approach and make this runnable for every case, even
        # if lessons are at nights
        section = Section.objects.get(teaches__teacher=teacher, day_of_lesson=now.weekday(),
                                      lesson_start__gt=(now - delta).time(), # or make equal to
                                      lesson_start__lt=(now + delta).time())
    except Section.DoesNotExist:
        return render(request, 'teacher/not_attendance_time.html')
    # TODO(aibeksmagulov): check if section was not already checked
    context = {'section': section, 'teacher': teacher}
    new_time = datetime.datetime.combine(now.date(), section.lesson_start)
    lesson_start_att_datetime = new_time - datetime.timedelta(minutes=20)
    # you may use F to compare inner fields
    if TeacherAttendance.objects.filter(section=section, date__gte=lesson_start_att_datetime).exists():
        return render(request, 'teacher/not_attendance_time.html')
    if request.method == 'POST':
        image_file = '.' # TODO(aibeksmagulov): path to an attendance photo, make it normal
        TeacherAttendance.objects.create(image_file=image_file, teacher=teacher, section=section)
        Enrolled.objects.filter(group=section.teaches.group, credits__gt=0).update(credits=F('credits') - 1)
        Group.objects.filter(pk=section.teaches.group_id).update(day=F('day') + 1)
        return render(request, 'teacher/successful_attend.html', context)
    else:
        return render(request, 'teacher/attend.html', context)

# TODO(aibeksmagulov): You didn't consider the case when there are more than one teacher assigned
# to one group, you should be able to derive sections correctly. Maybe it is not necessary,
# when we are doing attendance from one teacher
def _attend_student(request):
    student = get_object_or_404(Student, user=request.user)
    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes=20) # TODO(aibeksmagulov): change the delta
    try:
        inner_qs = Group.objects.filter(enrolled__student__user=student.user)
        # TODO(aibeksmagulov): maybe we should get rid of inner queries, by using explicit list() operator
        # BUG: if starting time of a lesson is 23:50 than it will not find what it should
        # TODO(aibeksmagulov): change the approach and make this runnable for every case, even
        # if lessons are at nights
        section = Section.objects.get(teaches__group__in=inner_qs, day_of_lesson=now.weekday(),
                                      lesson_start__gt=(now - delta).time(),  # or make equal to
                                      lesson_start__lt=(now + delta).time())
    except Section.DoesNotExist:
        return render(request, 'student/not_attendance_time.html')
    context = {'section': section, 'student': student}
    new_time = datetime.datetime.combine(now.date(), section.lesson_start)
    lesson_start_att_datetime = new_time - datetime.timedelta(minutes=20)
    # you may use F to compare inner fields
    if StudentAttendance.objects.filter(section=section,
                                        date__gte=lesson_start_att_datetime).exists():
        return render(request, 'student/not_attendance_time.html')
    if request.method == 'POST':
        StudentAttendance.objects.create(student=student, section=section)
        return render(request, 'student/successful_attend.html', context)
    else:
        return render(request, 'student/attend.html', context)


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