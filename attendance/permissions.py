from rest_framework import permissions

from user.models import Question


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 2:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.updated_by == request.user


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 1:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsHod(permissions.BasePermission):
    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if request.user.user_type == 3:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.updated_by == request.user
