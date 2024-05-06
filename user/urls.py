from django.contrib import admin
from django.urls import path, include

from user import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='user_registration'),
    path('login/', views.UserLoginView.as_view(), name='login'),

    path('viewquestion/', views.ViewQuestion.as_view(), name='view_question'),
    path('createquestion/', views.CreateQuestion.as_view(), name='create_question'),
    path('updatequestion/', views.UpdateQuestion.as_view(), name='update_question'),
    path('deletequestion/', views.DeleteQuestion.as_view(), name='delete_question'),

    path('viewcomment/', views.ViewComment.as_view(), name='view_comment'),
    path('createcomment/', views.PostComment.as_view(), name='view_comment'),
    path('deletecomment/', views.DeleteComment.as_view(), name='view_comment'),
    path('updateecomment/', views.UpdateComment.as_view(), name='view_comment'),


    path('comment/', views.PostComment.as_view(), name='comment'),

    path('viewstudent/<int:pk>', views.ViewStudentDetails.as_view(), name='view_student'),
    path('student/<int:id>/details/', views.PDFView.as_view(), name='student-details'),

]
