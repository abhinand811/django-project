from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from rest_framework import viewsets


class MyAccountManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Provide a valid email id")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOOSES = (
        (1, 'student'),
        (2, 'teacher'),
        (3, 'hod'),
        (4, 'principal'),
    )
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    user_type = models.PositiveIntegerField(choices=USER_TYPE_CHOOSES, default=1)
    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split('@')[0]

    def set_password(self, raw_password):
        password = make_password(raw_password)
        return password

    def save(self, *args, **kwargs):
        self.password = self.set_password(self.password)
        super(Account, self).save(*args, **kwargs)


class Teacher(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    experience = models.PositiveSmallIntegerField(default=0)


class Student(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    roll_no = models.PositiveSmallIntegerField
    dob = models.DateField(null=True, blank=True)
    guardian = models.CharField(max_length=225)


class Question(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    content = models.TextField()


class Comment(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()


class Department(models.Model):
    department_name = models.CharField(max_length=50)


class Hod(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    experience = models.PositiveSmallIntegerField(default=0)


class Management(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
