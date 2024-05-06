from django.urls import path, include

from mark import views

urlpatterns = [
    path('viewmark/', views.ViewMark.as_view(), name='view_mark'),
    path('createmark/', views.CreateMark.as_view(), name='create_question'),
    path('updatemark/', views.UpdateMark.as_view(), name='update_question'),
    path('deletemark/', views.DeleteMark.as_view(), name='delete_question'),
    ]
