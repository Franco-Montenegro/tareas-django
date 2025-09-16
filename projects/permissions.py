from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProjectOwnerOrReadOnly(BasePermission):
    """
    Solo el owner puede escribir; lectura permitida solo si el objeto es del owner (lo filtramos en queryset).
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.owner == request.user
        return obj.owner == request.user

class CanEditTask(BasePermission):
    """
    Puede editar la tarea el owner del proyecto o el usuario asignado.
    Lectura: la restringimos por queryset (ver ViewSet).
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            # Lectura ya viene filtrada por queryset
            return True
        return (obj.project.owner == request.user) or (obj.assigned_to == request.user)

class IsCommentAuthorOrProjectOwnerOrReadOnly(BasePermission):
    """
    Puede editar/eliminar el comentario el autor o el owner del proyecto.
    Lectura: controlada por queryset.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (obj.user == request.user) or (obj.task.project.owner == request.user)
