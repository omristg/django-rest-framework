from rest_framework import serializers
from watchlist_app.models import Review, WatchList, StreamPlatform


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['watchlist']


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    platform_name = serializers.SerializerMethodField()

    class Meta:
        model = WatchList
        fields = ['id', 'title', 'storyline', 'active', 'created',
                  'platform', 'platform_name', 'reviews']

    def get_platform_name(self, object):
        return object.platform.name


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    # Types of serializers relations
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watchlist-details'
    # )
    # watchlist = serializers.HyperlinkedIdentityField(view_name='watchlist-details', many=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'
