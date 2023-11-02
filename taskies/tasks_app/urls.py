from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.getTasks, name='tasks'), # GET ALL TASKS
    path('users/', views.getUsers, name='users'), # GET ALL USERS
    path('tasks/<int:id>/', views.getTaskById, name='taskById'), # GET ONE TASK BY ID
    path('users/<int:id>/', views.getUserById, name='userById'), # GET ONE USER BY ID
    path('postTask/', views.postTask, name='postTask'), # POST TASK
    path('postUser/', views.postUser, name='postUser'), # POST USER
]