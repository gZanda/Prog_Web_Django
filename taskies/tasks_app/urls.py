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

    re_path('userLogin/' , views.login),                                        # Login - All
    re_path('userSignin/' , views.signin),                                      # Signin - Managers
    re_path('userTest/' , views.test),              # Só teste do Token
    re_path('userLogout/' , views.logout),                                      # Logout - All   
]