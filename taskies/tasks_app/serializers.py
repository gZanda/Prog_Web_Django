# Serializer : File that will convert the Python objects into JSON 

from rest_framework import serializers
from .models import Task
from .models import User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email','password','role')
        extra_kwargs = {'password': {'write_only': True}}