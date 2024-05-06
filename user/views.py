import json
from io import BytesIO

from celery import shared_task
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from reportlab.pdfgen import canvas
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, views, status, viewsets
# from rest_framework.request.Request import user
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.views import LoginView

from attendance.models import StudentAttendance
from mark.models import Mark
from user.models import Question, Comment, Account, Student
from user.permissions import IsStudentOfTeacher, IsTeacher, IsStudent
from user.serializers import UserSerializer, QuestionSerializer, CommentSerializer, StudentSerializer
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .serializers import StudentSerializer
from .models import Student


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserLoginView(views.APIView):

    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)

        return Response({'msg': 'Login Success'}, status=status.HTTP_200_OK)


class ViewQuestion(generics.ListAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        student_teacher_id = self.request.user.student.teacher_id
        queryset = queryset.filter(teacher_id=student_teacher_id)
        return queryset

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, IsStudentOfTeacher | IsTeacher)


class CreateQuestion(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, IsTeacher,)


class UpdateQuestion(generics.UpdateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)


class DeleteQuestion(generics.DestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, IsTeacher,)


class PostComment(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsStudentOfTeacher)

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.save)
        return Response({
            "status": status.HTTP_200_OK,
            'message': 'Comment added successfully',
            'data': serializer.data
        })


class ViewComment(generics.ListAPIView):
    def get_queryset(self):
        question_id = int(self.request.query_params.get('question_id'))
        print()
        queryset = Comment.objects.filter(question_id=question_id)
        return queryset

    queryset = Comment.objects.all()
    print(queryset)
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsStudentOfTeacher | IsTeacher)


class UpdateComment(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsStudent)


class DeleteComment(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsStudent | IsTeacher)


# class GenerateStudentReport(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         user = request.user
#
#     account = Account.objects.get(user=user)
#     student = Student.objects.get(user_id=user)
#     mark = Mark.objects.get(student_id=student)
#     attendance = StudentAttendance.objects.get(student_id=student)


class ViewStudentDetails(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #
    # account = Account.objects.get(user=user)
    # student = Student.objects.get(user_id=user)
    # mark = Mark.objects.get(student_id=student)
    # attendance = StudentAttendance.objects.get(student_id=student)


class PDFView(APIView):
    def get(self, request, *args, **kwargs):
        self.generate_pdf(kwargs['id'])
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = \
            f'attachment; filename="transcript_abhinand.pdf"'
        response.write(p.read())

        return response

    def generate_pdf(self, id):
        user = Student.objects.get(id=id)
        serializer = StudentSerializer(user)
        data = json.dumps(serializer.data)
        p = canvas.Canvas('report_' + user.name.lower() + '.pdf')

        p.drawString(100, 700, data)

        p.showPage()
        p.save()
        return p
