
from django.urls import path
from watchlist_app.api.views import WatchDetailAV, WatchListAV

urlpatterns = [
    path('', WatchListAV.as_view(), name='watchlist-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='watchlist-details')
]
