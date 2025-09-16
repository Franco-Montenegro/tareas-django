from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Task, Comment

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserMiniSerializer(read_only=True)
    tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = ("id", "name", "description", "created_at", "owner", "tasks_count")

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, required=False
    )
    assigned_to_detail = UserMiniSerializer(source="assigned_to", read_only=True)

    class Meta:
        model = Task
        fields = (
            "id", "project", "title", "description", "status",
            "assigned_to", "assigned_to_detail", "created_at"
        )

class CommentSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    user = UserMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "task", "user", "content", "created_at")
