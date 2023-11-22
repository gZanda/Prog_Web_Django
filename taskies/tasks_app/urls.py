from django.urls import path, re_path
from . import views

urlpatterns = [
    path('tasks/', views.getTasks, name='tasks'),                               # Get all Tasks - All
    path('tasks/<int:id>/', views.getTaskById, name='taskById'),                # Get one Task - All
    path('createTask/', views.postTask, name='postTask'),                       # Create Task - Manager
    path('deleteTask/<int:id>/', views.deleteTaskById, name='deleteTaskById'),  # Delete Task - Manager
    path('editTask/<int:id>/', views.putTaskById, name='putTaskById'),          # Update Task - All

    path('users/', views.getUsers, name='users'),                               # Get All Users - Manager
    path('users/<int:id>/', views.getUserById, name='userById'),                # Get one User - Manager
    path('deleteUser/<int:id>/', views.deleteUserById, name='deleteUserById'),  # Delete User - Manager

    re_path('login/' , views.login),                                        # Login - All
    re_path('signin/' , views.signin),                                      # Signin - Managers
    re_path('test/' , views.test),              # Só teste do Token
    re_path('logout/' , views.logout),                                      # Logout - All
    
]