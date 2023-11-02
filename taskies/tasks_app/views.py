# Views: Functions that handle the request and return a response

from .serializers import TaskSerializer, UserSerializer
from .models import Task, User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# GET ALL USERS
@api_view(['GET'])
def getTasks(request):
    tasks = Task.objects.all()                                      # Get all tasks from the database
    serializer = TaskSerializer(tasks, many=True)                   # Convert the tasks to JSON
    return Response(serializer.data, status=status.HTTP_200_OK)     # Return the JSON