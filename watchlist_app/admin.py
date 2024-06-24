from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin


from watchlist_app.models import Organization, OrganizationAPIKey
from watchlist_app.models import Review, StreamPlatform, WatchList


admin.site.register(WatchList)
admin.site.register(StreamPlatform)
admin.site.register(Review)
admin.site.register(Organization)


@admin.register(OrganizationAPIKey)
class OrganizationAPIKeyModelAdmin(APIKeyModelAdmin):
    pass
