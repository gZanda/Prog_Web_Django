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

# GET ONE TASK BY ID - Receives id via URL
@api_view(['GET'])
def getTaskById(request, id):
    try:
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# GET ONE USER BY ID - Receives id via URL
@api_view(['GET'])
def getUserById(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# POST TASK
@api_view(['POST'])
def postTask(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# POST USER
@api_view(['POST'])
def postUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# DELETE TASK BY ID - Receives id via URL
@api_view(['DELETE'])
def deleteTaskById(request, id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# DELETE USER BY ID - Receives id via URL
@api_view(['DELETE'])
def deleteUserById(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)