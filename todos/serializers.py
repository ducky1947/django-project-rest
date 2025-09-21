from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class TodoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'description', 'completed', 'priority', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class TodoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'completed', 'priority', 'due_date']
