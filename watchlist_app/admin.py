from django.contrib import admin

from watchlist_app.models import StreamPlatform, WatchList

admin.site.register(WatchList)
admin.site.register(StreamPlatform)
