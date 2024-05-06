from django.urls import path, include

from attendance import views

urlpatterns = [
    path('viewattendance/student', views.ViewStudentAttendance.as_view(), name='view_student_attendance'),
    path('createattendance/student', views.CreateStudentAttendance.as_view(), name='create_student_attendance'),
    path('updateattendance/student/<int:pk>', views.UpdateStudentAttendance.as_view(), name='update_student_attendance'),

    path('viewattendance/teacher', views.ViewTeacherAttendance.as_view(), name='view_teacher_attendance'),
    path('createattendance/teacher', views.CreateTeacherAttendance.as_view(), name='create_teacher_attendance'),
    path('updateattendance/teacher/<int:pk>', views.UpdateStudentAttendance.as_view(),
         name='update_teacher_attendance'),
    ]