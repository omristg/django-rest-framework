from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework import permissions, generics
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.decorators import action, api_view

from .permissions import HasOrganizationAPIKey
from watchlist_app.models import OrganizationAPIKey
from watchlist_app.api.permissions import IsReviewOwnerOrReadOnlyOrAdmin
from watchlist_app.models import (
    WatchList,
    StreamPlatform,
    Review,
    Organization,
)
from watchlist_app.api.serializers import (
    WatchListSerializer,
    StreamPlatformSerializer,
    ReviewSerializer,
)


class ReviewList(generics.ListAPIView):
    def get_queryset(self):
        watchlist_pk = self.kwargs.get("pk")
        return Review.objects.filter(watchlist=watchlist_pk)

    serializer_class = ReviewSerializer


class ReviewCreate(generics.CreateAPIView):
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        watchlist_pk = self.kwargs.get("pk")
        watchlist = WatchList.objects.get(pk=watchlist_pk)

        current_user = self.request.user
        existing_reviews = Review.objects.filter(
            watchlist=watchlist, review_user=current_user
        )
        if existing_reviews.exists():
            raise ValidationError("You cannot submit more reviews to this item")

        serializer.save(watchlist=watchlist, review_user=current_user)

    serializer_class = ReviewSerializer


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnlyOrAdmin]


class StreamPlatformViewSet(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


# Option for  ModelViewSet on same StreamPlatform


class StreamPlatformAV(APIView):
    def get(self, request):
        items = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailsAV(APIView):
    def get(self, request, pk):
        try:
            item = StreamPlatform.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            item = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = StreamPlatformSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            item = StreamPlatform.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        watchlists = WatchList.objects.all()
        serializer = WatchListSerializer(watchlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailAV(APIView):
    def get(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(
                {"error": "Watchlist not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request, pk):
        watchlist = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        watchlist = WatchList.objects.get(pk=pk)
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizationListView(APIView):
    permission_classes = [HasOrganizationAPIKey]

    def get(self, request):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = OrganizationAPIKey.objects.get_from_key(key)
        res = api_key.organization
        return Response({"organization": res.name})

    def post(self, request):
        org_name = request.data["name"]
        org = Organization.objects.get(name=org_name)
        api_key, key = OrganizationAPIKey.objects.create_key(
            name=f"{org_name}-key", organization=org
        )
        return Response({"key": key})

    def delete(self, request):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = OrganizationAPIKey.objects.get_from_key(key)
        print("hihi")
        api_key.revoked = True
        api_key.save()
        return Response({"message": "Key revoked"})

    @api_view(["GET"])
    def test2(request):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_keys = OrganizationAPIKey.objects.get_usable_keys()
        for key in api_keys:
            print(key.id)
        return Response({"valid keys": "od"})


class TestView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        return Response({"message": "Hello, World!"})


def test_view(request):
    #  context = {
    #     'subject': 'Sample Subject',
    #     'message': 'This is a sample message.',
    # }
    return render(request, "test.html")
