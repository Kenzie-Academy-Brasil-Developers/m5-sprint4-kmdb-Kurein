from rest_framework.permissions import BasePermission
from rest_framework.views import Request


class MoviesPermission(BasePermission):
    def has_permission(self, request: Request, _):
        admin_methods = {
            "POST",
            "PATCH",
            "DELETE",
        }

        if request.method in admin_methods:
            return request.user.is_superuser

        return True