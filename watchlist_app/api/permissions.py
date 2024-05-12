from rest_framework import permissions


class IsReviewOwnerOrReadOnlyOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True

        return obj.review_user == request.user
