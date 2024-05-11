
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import *

router = DefaultRouter()
router.register(r'stream-alt', StreamPlatformViewSet, basename='stream-alt')
# Option for ModelViewSet

urlpatterns = [

    path('list/', WatchListAV.as_view(), name='watchlist-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='watchlist-details'),

    path('', include(router.urls)),
    # Option for ModelViewSet

    path('stream/', StreamPlatformAV.as_view(), name='stream-platform-list'),
    path('stream/<int:pk>', StreamPlatformDetailsAV.as_view(),
         name='stream-platform-details'),

    path('<int:pk>/review', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create', ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
]
