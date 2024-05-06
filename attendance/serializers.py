from rest_framework import serializers

from attendance.models import Attendance, StudentAttendance, TeacherAttendance
from mark.models import Mark


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['atendee', 'atendee_type']


def validate(self, attrs):
    if attrs['atendee_type'] != 1:
        raise serializers.ValidationError({'atendee_type': 'Given user is not a student.'})
    elif attrs['atendee_type'] != 2:
        raise serializers.ValidationError({'atendee_type': 'Given user is not a teacher.'})
    return attrs


class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = ['student', 'date', 'is_present']


class TeacherAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = ['teacher', 'date', 'is_present']
