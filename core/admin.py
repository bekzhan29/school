from django.contrib import admin
from .models import Student, Teacher, Group, Enrolled, Office, Section, Teaches, Payment, \
    TeacherAttendance, StudentAttendance

models_to_register = [Student, Teacher, Group, Enrolled, Office, Section, Teaches, Payment,
                      TeacherAttendance, StudentAttendance]
admin.site.register(models_to_register)