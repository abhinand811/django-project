from django.db import models

from user.models import Student, Teacher, Account


class Attendance(models.Model):
    atendee = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, related_name="attender")
    atendee_type = models.IntegerField()
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE)


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE)


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE)

