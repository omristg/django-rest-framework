from rest_framework import permissions
from rest_framework_api_key.permissions import BaseHasAPIKey
from watchlist_app.models import OrganizationAPIKey


class IsReviewOwnerOrReadOnlyOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True

        return obj.review_user == request.user


class HasOrganizationAPIKey(BaseHasAPIKey):
    model = OrganizationAPIKey
