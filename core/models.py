from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    # TODO(aibeksmagulov): add the validation for phone number
    phone_num = models.CharField(max_length=20)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' @' + self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    # TODO(aibeksmagulov): change this to be able to send SMS in future, also make use of
    # form validation.
    phone_num = models.CharField(max_length=20)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' @' + self.user.username


class Group(models.Model):
    name = models.CharField(max_length=40, unique=True)
    capacity = models.IntegerField(default=0)
    max_capacity = models.IntegerField()
    price = models.IntegerField()
    day = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Enrolled(models.Model):
    # TODO(aibeksmagulov): what will be the results of a table if we update the tables on which
    # foreign keys points to? Check this thoroughly.
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group)
    registration_date = models.DateField(auto_now_add=True)
    credits = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Enrolled"
        verbose_name_plural = "Enrolled"

    def __str__(self):
        return '@' + self.student.user.username + ' in ' + self.group.name


class Payment(models.Model):
    student = models.ForeignKey(Student)
    group = models.ForeignKey(Group)
    date_of_payment = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    # TODO(aibeksmagulov): is the following correct?
    recipient = models.ForeignKey(User)

    def __str__(self):
        return '@' + self.student.user.username + ' ' + self.group.name + ' ' + self.date_of_payment


class Office(models.Model):
    name = models.CharField(max_length=40, unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    # TODO(aibeksmagulov): add the validation for phone number
    phone_num = models.CharField(max_length=20)
    rent = models.IntegerField()

    def __str__(self):
        return self.name


class Teaches(models.Model):
    # TODO(aibeksmagulov): add conditions for foreign keys, on_delete, on_update
    teacher = models.ForeignKey(Teacher)
    group = models.ForeignKey(Group)
    salary = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Teaches"
        verbose_name_plural = "Teaches"

    def __str__(self):
        return '@' + self.teacher.user.username + ' at ' + self.group.name


class Section(models.Model):
    teaches = models.ForeignKey(Teaches)
    office = models.ForeignKey(Office)
    duration = models.IntegerField(default=120) # in minutes
    lesson_start = models.TimeField()
    lesson_end = models.TimeField()
    day_of_lesson = models.CharField(max_length=3)

    def __str__(self):
        return '@' + self.teaches.teacher.user.username + ' in ' + \
               self.teaches.group.name + ' at ' + self.office.name + ' on ' + self.day_of_lesson + \
               ' ' + self.lesson_start.isoformat() + ' - ' + self.lesson_end.isoformat()


class Attendance(models.Model):
    image_file = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher)
    section = models.ForeignKey(Section)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"