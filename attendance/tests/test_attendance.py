from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from user.models import Student, Teacher


class TestAttendance(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = get_user_model().objects.create_user(
            email='teacher@example.com',
            password='aaaaaaaa',
            name='teacher',
            phone_number="7896541230",
            user_type=2
        )
        self.client.login(email="teacher@example.com", password="aaaaaaaa")
        self.access_token_teacher = AccessToken.for_user(self.teacher)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')

        self.student = get_user_model().objects.create_user(
            email='student@example.com',
            password='aaaaaaaa',
            name='student',
            phone_number="7896541230",
            user_type=1
        )
        print(self.student.id)
        self.client.login(email="student@example.com", password="aaaaaaaa")
        self.access_token_teacher = AccessToken.for_user(self.teacher)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')



    def test_create_student_teacher(self):
        # teacher_id = Teacher.objects.all()
        # print("teacher_id",teacher_id)
        l = Teacher.objects.create(
            subject="english",
            experience=2,
            user_id=1
        )
        Student.objects.create(
            guardian="dkhsdks",
            dob="2025-05-25",
            teacher_id=l.id,
            user_id=2
        )
        attendance = {
            "date": "2024-05-26",
            "is_present": 1,
            "student": 1,
        }

        response = self.client.post('/api/attendance/createattendance/student', attendance, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)



