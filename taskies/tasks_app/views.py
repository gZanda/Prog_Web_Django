# Views: Functions that handle the request and return a response

from django.contrib.auth.hashers import make_password
from .serializers import TaskSerializer, UserSerializer
from .models import Task, User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from jobs.sender import send_to_queue
# Token imports
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
# Authentication imports
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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

# --------------------------------------------------------------------------------------------

# User Login with Token
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email']) # Get user by email
    if not user.check_password(request.data['password']):       # Check password
        return Response({'detail': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)   # if password is wrong
    token, created = Token.objects.get_or_create(user=user)     # Get Token or Recreate Token
    serializer = UserSerializer(instance=user)             # Serialize user
    return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK) # Return token and user


# User Signin with Token
@api_view(['POST'])
def signin(request):
    serializer = UserSerializer(data=request.data) # Serialize user
    if serializer.is_valid():                       # Check if user json data is valid
        email = serializer.validated_data['email']  # Validate email
        password = make_password(serializer.validated_data['password'])     # Hash the password before saving
        serializer.save(password=password)  # Save the hashed password
        # token = Token.objects.create(user=serializer.instance) # Create token
        return Response(serializer.data, status=status.HTTP_201_CREATED) # Return token and user
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # If user is not valid

# User token validation test
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication]) # Check if token is valid
@permission_classes([IsAuthenticated]) # Check if user is authenticated
def test(request):
    return Response("Valid token for {}".format(request.user.email))

# User logout with Token
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication]) # Check if token is valid
@permission_classes([IsAuthenticated])  # Check if user is authenticated
def logout(request):
    request.user.auth_token.delete() # Delete user token
    return Response("{} Logged out".format(request.user.email),status=status.HTTP_200_OK) 