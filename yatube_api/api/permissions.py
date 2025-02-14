from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """Предоставляет доступ к объекту только его автору."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
