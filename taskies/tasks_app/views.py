# Views: Functions that handle the request and return a response

from django.contrib.auth.hashers import make_password
from .serializers import TaskSerializer, UserSerializer
from .models import Task, User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from jobs.sender import send_to_queue
# Token imports
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
# Authentication imports
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated       
    
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

# User Signin (no token here )
@api_view(['POST'])
def signin(request):
    serializer = UserSerializer(data=request.data) # Serialize user
    if serializer.is_valid():                       # Check if user json data is valid
        email = serializer.validated_data['email']  # Validate email
        password = make_password(serializer.validated_data['password'])     # Hash the password before saving
        serializer.save(password=password)  # Save the hashed password
        print(email)
        send_to_queue(email) # Send email using Rabit
        return Response(serializer.data, status=status.HTTP_201_CREATED) # Return token and user
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # If user is not valid

# Token related --------------------------------------------------------------------------------------------

# User Token Test
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication]) # Check if token is valid
@permission_classes([IsAuthenticated]) # Check if user is authenticated
def test(request):
    return Response("Valid token for {}".format(request.user.email))

# User Login with Token -> All users
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email']) # Get user by email
    if not user.check_password(request.data['password']):       # Check password
        return Response({'detail': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)   # if password is wrong
    token, created = Token.objects.get_or_create(user=user)     # Get Token or Recreate Token
    serializer = UserSerializer(instance=user)             # Serialize user
    return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK) # Return token and user

# User logout with Token -> All users
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication]) # Check if token is valid
@permission_classes([IsAuthenticated])  # Check if user is authenticated
def logout(request):
    request.user.auth_token.delete() # Delete user token
    return Response("{} Logged out".format(request.user.email),status=status.HTTP_200_OK) 
    
# Get all Tasks -> All Users (Managers can see all, Workers can see only theirs)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getTasks(request):
    if request.user.role == "Manager":
        try:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            tasks = Task.objects.filter(responsible=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
# Create Task -> Only Managers
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def postTask(request):
    if request.user.role == "Manager":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("User is not a Manager", status=status.HTTP_404_NOT_FOUND)
    
# Delete Task by id -> Only Managers
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteTaskById(request, id):
    if request.user.role == "Manager":
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return Response("Task Deleted",status=status.HTTP_200_OK)
        except:
            return Response("Task not Found",status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("User is not a Manager", status=status.HTTP_404_NOT_FOUND)
    
# Get one Task by id -> All Users (Managers can see all, Workers can see only theirs)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getTaskById(request, id):
    if request.user.role == "Manager":
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            task = Task.objects.get(id=id, responsible=request.user)
            serializer = TaskSerializer(task, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
# Get all Users -> Only Managers
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUsers(request):
    if request.user.role == "Manager":
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("User is not a Manager", status=status.HTTP_404_NOT_FOUND)
    
# Get one User by id -> Only Managers
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUserById(request, id):
    if request.user.role == "Manager":
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("User is not a Manager", status=status.HTTP_404_NOT_FOUND)
    
# Edit Task by id -> All Users (Managers can edit all, Workers can edit only theirs)
@api_view(['PUT'])
def putTaskById(request, id):
    if request.user.role == "Manager":
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(instance=task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            task = Task.objects.get(id=id, responsible=request.user)
            serializer = TaskSerializer(instance=task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)