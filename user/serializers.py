from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from attendance.serializers import  StudentAttendanceSerializer
from mark.serializers import MarkSerializer
from .models import Question, Comment, Student
from rest_framework import serializers, exceptions


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        max_length=100, write_only=True, required=False
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'confirm_password', 'phone_number', 'name', 'user_type', 'is_staff',
                  'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'confirm_password': {'write_only': True, 'min_length': 5}
        }

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return get_user_model().objects.create_user(**validated_data)

    def validate(self, attrs):
        if attrs.get('password') == attrs.get('confirm_password'):
            return attrs
        raise exceptions.ValidationError('need same passwd')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


# class CreateQuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'question']


class StudentSerializer(serializers.ModelSerializer):
    marks = MarkSerializer(many=True, read_only=True)
    attendance = StudentAttendanceSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['guardian', 'dob', 'teacher', 'marks', 'attendance']
