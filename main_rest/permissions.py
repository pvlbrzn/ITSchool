from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManagerOrReadOnly(BasePermission):
    """
    Permission class that allows read-only access to any user,
    and write access only to superusers or users in the 'managers' group.
    """

    def has_permission(self, request, view):
        """
        Return True if request is read-only (safe) or user has manager rights.
        """
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return (
            user.is_authenticated and
            (user.is_superuser or user.groups.filter(name='managers').exists())
        )


class IsManager(BasePermission):
    """
        Permission class that allows access only to superusers or users in the 'managers' group.
    """

    def has_permission(self, request, view):
        """
        Return True if user is authenticated and has manager rights.
        """
        user = request.user
        return (
                user.is_authenticated and
                (user.is_superuser or user.groups.filter(name='managers').exists())
        )
