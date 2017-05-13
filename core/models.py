from django.contrib.auth.models import User
from django.db import models
import calendar
from django.utils.timezone import localtime


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
    total_lessons = models.IntegerField(default=36) # TODO(aibeksmagulov): make migrations

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

# TODO(aibeksmagulov): put constraints that we can not have two lessons for one teacher at
# intersecting times, or that we can not have more than one group at the same office intersecting.
# We can have two teachers at the same group during one time.
class Section(models.Model):
    teaches = models.ForeignKey(Teaches)
    office = models.ForeignKey(Office)
    duration = models.IntegerField(default=120) # in minutes
    lesson_start = models.TimeField()
    lesson_end = models.TimeField()
    day_of_lesson = models.IntegerField()

    def __str__(self):
        return '@' + self.teaches.teacher.user.username + ' in ' + \
               self.teaches.group.name + ' at ' + self.office.name + ' on ' + \
               calendar.day_name[self.day_of_lesson] + ' ' + self.lesson_start.isoformat() + \
                                 ' - ' + self.lesson_end.isoformat()


class TeacherAttendance(models.Model):
    image_file = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher)
    section = models.ForeignKey(Section)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "TeacherAttendance"
        verbose_name_plural = "TeacherAttendance"

    def __str__(self):
        local = localtime(self.date).replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
        return self.section.__str__() + ' (' + local.__str__() + ')'


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student)
    section = models.ForeignKey(Section)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "StudentAttendance"
        verbose_name_plural = "StudentAttendance"

    def __str__(self):
        local = localtime(self.date).replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
        # TODO(aibeksmagulov): change __str__ representation
        return self.section.__str__() + ' (' + local.__str__() + ')'
