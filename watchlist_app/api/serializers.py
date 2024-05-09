from rest_framework import serializers
from watchlist_app.models import WatchList


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = '__all__'
