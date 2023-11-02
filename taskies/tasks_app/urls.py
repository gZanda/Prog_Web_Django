from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.getTasks, name='tasks'), # GET ALL TASKS
    path('users/', views.getUsers, name='users'), # GET ALL USERS
]