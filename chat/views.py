from django.shortcuts import render

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import Room
from chat.permissions import CanCreateRoom
from chat.serializers import RoomSerializer


def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })


class CreateRoomView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, CanCreateRoom)

    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Student room created successfully.',
            'data': serializer.data
        })

