# Views: Functions that handle the request and return a response

from .serializers import TaskSerializer, UserSerializer
from .models import Task, User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# GET ALL TASKS
@api_view(['GET'])  
def getTasks(request):
    tasks = Task.objects.all()                                      
    serializer = TaskSerializer(tasks, many=True)                   
    return Response(serializer.data, status=status.HTTP_200_OK)     

# GET ALL USERS
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()                                      
    serializer = UserSerializer(users, many=True)                   
    return Response(serializer.data, status=status.HTTP_200_OK)     

# GET ONE TASK BY ID - Receives the id as a parameter by the URL
@api_view(['GET'])
def getTaskById(request, id):
    try:
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# GET ONE USER BY ID - Receives the id as a parameter by the URL
@api_view(['GET'])
def getUserById(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)