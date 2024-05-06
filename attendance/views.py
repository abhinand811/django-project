from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from attendance.models import Attendance, StudentAttendance, TeacherAttendance
from attendance.serializers import AttendanceSerializer, StudentAttendanceSerializer, TeacherAttendanceSerializer
from attendance.permissions import IsStudent, IsHod, IsTeacher


class ViewAttendance(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated,)


class CreateAttendance(generics.CreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated, IsTeacher | IsHod)

    def post(self, request, *args, **kwargs):
        serializer = AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response({
            "status": status.HTTP_200_OK,
            'message': 'Comment added successfully',
            'data': serializer.data
        })


class UpdateAttendance(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated, IsTeacher | IsHod)


class ViewStudentAttendance(generics.ListAPIView):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    permission_classes = (IsAuthenticated,)


class CreateStudentAttendance(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        serializer = StudentAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response({
            "status": status.HTTP_200_OK,
            'message': 'Attendance added successfully',
            'data': serializer.data
        })


class UpdateStudentAttendance(generics.UpdateAPIView):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    permission_classes = (IsAuthenticated, IsTeacher)


class ViewTeacherAttendance(generics.ListAPIView):
    serializer_class = TeacherAttendanceSerializer
    permission_classes = (IsAuthenticated,)


class CreateTeacherAttendance(generics.CreateAPIView):
    serializer_class = TeacherAttendanceSerializer
    permission_classes = (IsAuthenticated, IsHod)

    def post(self, request, *args, **kwargs):
        serializer = StudentAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response({
            "status": status.HTTP_200_OK,
            'message': 'Attendance added successfully',
            'data': serializer.data
        })


class UpdateTeacherAttendance(generics.UpdateAPIView):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceSerializer
    permission_classes = (IsAuthenticated, IsHod)
