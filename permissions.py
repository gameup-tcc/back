from rest_framework import permissions

class SafeMethodsPermission(permission.BasePermission):
    def has_permission(self, request, view):
        return self.has_object_permission(request, view)

    def has_object_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
