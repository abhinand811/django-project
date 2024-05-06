from rest_framework import serializers

from mark.models import Mark


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['student', 'subject_a', 'subject_b', 'subject_c', 'student']
