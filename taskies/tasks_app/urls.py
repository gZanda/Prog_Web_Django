from django.urls import path, re_path
from . import views

urlpatterns = [
    path('tasks/', views.getTasks, name='tasks'),                               # Get all Tasks
    path('tasks/<int:id>/', views.getTaskById, name='taskById'),                # Get one Task
    path('createTask/', views.postTask, name='postTask'),                       # Create Task
    path('deleteTask/<int:id>/', views.deleteTaskById, name='deleteTaskById'),  # Delete Task     
    path('editTask/<int:id>/', views.putTaskById, name='putTaskById'),          # Update Task

    path('users/', views.getUsers, name='users'),                               # Get All Users
    path('users/<int:id>/', views.getUserById, name='userById'),                # Get one User
    path('editUser/<int:id>/', views.putUserById, name='putUserById'),          # Update User
    path('deleteUser/<int:id>/', views.deleteUserById, name='deleteUserById'),  # Delete User

    re_path('userLogin/' , views.login),
    re_path('userSignin/' , views.signin),
    re_path('userTest/' , views.test),
    re_path('userLogout/' , views.logout),
    re_path('allUserTasks/', views.allUserTasks),
    
]