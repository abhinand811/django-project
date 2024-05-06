from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mark.models import Mark
from mark.serializers import MarkSerializer
from user.models import Teacher
from user.permissions import IsTeacher, IsHod


class CreateMark(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        serializer = MarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = Teacher.objects.get(user=request.user)
        serializer.save(teacher=teacher)
        return Response({
            "status": status.HTTP_200_OK,
            'message': 'Comment added successfully',
            'data': serializer.data
        })


class ViewMark(generics.ListAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    permission_classes = (IsAuthenticated,)


class UpdateMark(generics.UpdateAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    permission_classes = (IsAuthenticated, IsTeacher)


class DeleteMark(generics.DestroyAPIView):
    serializer_class = MarkSerializer
    permission_classes = (IsAuthenticated, IsTeacher | IsHod)
