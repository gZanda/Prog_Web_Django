# Views: Functions that handle the request and return a response

from django.contrib.auth.hashers import make_password
from .serializers import TaskSerializer, UserSerializer, UserLoginSerializer
from .models import Task, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from jobs.sender import send_to_queue

# Get all Tasks
@api_view(['GET'])  
def getTasks(request):
    tasks = Task.objects.all()                                      
    serializer = TaskSerializer(tasks, many=True)                   
    return Response(serializer.data, status=status.HTTP_200_OK)         

# Get one Task by id
@api_view(['GET'])
def getTaskById(request, id):
    try:
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# Create Task
@api_view(['POST'])
def postTask(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# Delete Task by id
@api_view(['DELETE'])
def deleteTaskById(request, id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# Edit Task by id
@api_view(['PUT'])
def putTaskById(request, id):
    try:
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# Get all Users
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()                                      
    serializer = UserSerializer(users, many=True)                   
    return Response(serializer.data, status=status.HTTP_200_OK) 

# Get one User by id
@api_view(['GET'])
def getUserById(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# Delete User by id
@api_view(['DELETE'])
def deleteUserById(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# Edit User by id
@api_view(['PUT'])
def putUserById(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# Create User    
@api_view(['POST'])
@permission_classes([AllowAny])
def userRegistration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Hash the password before saving
        email = serializer.validated_data['email']
        password = make_password(serializer.validated_data['password'])
        serializer.save(password=password)  # Set the hashed password
        print(email)
        send_to_queue(email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login User
@api_view(['POST'])
@permission_classes([AllowAny])
def userLogin(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        print(f'email: {email} Password: {password}')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
