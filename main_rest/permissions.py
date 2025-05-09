from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManagerOrReadOnly(BasePermission):
    """
    Разрешает безопасные методы (GET, HEAD, OPTIONS) всем,
    а POST, PUT, DELETE — только суперпользователям или пользователям из группы 'managers'.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return (
            user.is_authenticated and
            (user.is_superuser or user.groups.filter(name='managers').exists())
        )


class IsManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
                user.is_authenticated and
                (user.is_superuser or user.groups.filter(name='managers').exists())
        )
