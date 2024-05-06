from django.db import models

from user.models import Teacher


class Mark(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='mark_teacher')
    student = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name='mark_student')
    subject_a = models.PositiveSmallIntegerField()
    subject_b = models.PositiveSmallIntegerField()
    subject_c = models.PositiveSmallIntegerField()
