from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.getTasks, name='tasks'), # GET ALL TASKS
    path('users/', views.getUsers, name='users'), # GET ALL USERS
    path('tasks/<int:id>/', views.getTaskById, name='taskById'), # GET TASK 
    path('users/<int:id>/', views.getUserById, name='userById'), # GET USER 
    path('postTask/', views.postTask, name='postTask'), # POST TASK
    path('postUser/', views.postUser, name='postUser'), # POST USER
    path('deleteTask/<int:id>/', views.deleteTaskById, name='deleteTaskById'), # DELETE TASK    
    path('deleteUser/<int:id>/', views.deleteUserById, name='deleteUserById'), # DELETE USER 
    path('putTask/<int:id>/', views.putTaskById, name='putTaskById'), # UPDATE TASK 
    path('putUser/<int:id>/', views.putUserById, name='putUserById'), # UPDATE USER 
    path('betterCreateUser/', views.userRegistration, name='userRegistration'), # BETTER CREATE USER
    path('betterUserLogin/', views.userLogin, name='userLogin'), # BETTER USER LOGIN
]