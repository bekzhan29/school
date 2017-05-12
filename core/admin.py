from django.contrib import admin
from .models import Student, Teacher, Group, Enrolled, Office

models_to_register = [Student, Teacher, Group, Enrolled, Office]
admin.site.register(models_to_register)