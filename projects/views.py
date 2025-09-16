from django.db.models import Count, Q
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from .permissions import IsProjectOwnerOrReadOnly, CanEditTask, IsCommentAuthorOrProjectOwnerOrReadOnly

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwnerOrReadOnly]
    filterset_fields = ["name"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        # Solo proyectos del usuario autenticado
        return (
            Project.objects.filter(owner=self.request.user)
            .annotate(tasks_count=Count("tasks"))
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, CanEditTask]
    filterset_fields = ["status", "project", "assigned_to"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        # Puede ver tareas:
        # - de proyectos donde es owner
        # - o en las que está asignado
        return Task.objects.filter(
            Q(project__owner=user) | Q(assigned_to=user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        # Solo el owner del proyecto puede crear tareas en ese proyecto
        if project.owner != self.request.user:
            raise PermissionDenied("No puedes crear tareas en proyectos que no te pertenecen.")
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthorOrProjectOwnerOrReadOnly]
    filterset_fields = ["task"]
    search_fields = ["content"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        # Ver comentarios de tareas en proyectos del owner o tareas donde estás asignado
        return Comment.objects.filter(
            Q(task__project__owner=user) | Q(task__assigned_to=user)
        ).select_related("task", "user", "task__project")

    def perform_create(self, serializer):
        task = serializer.validated_data["task"]
        user = self.request.user
        # Solo puedes comentar si eres owner del proyecto o estás asignado a la tarea
        if not (task.project.owner == user or task.assigned_to == user):
            raise PermissionDenied("No puedes comentar en tareas que no te pertenecen ni te asignaron.")
        serializer.save(user=user)
