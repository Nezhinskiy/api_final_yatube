from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
        )


# class IsAdminUserOrReadOnly(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         return request.user == request.user.is_staff
#
#     def has_object_permission(self, request, view, obj):
#         return request.user == request.user.is_staff
