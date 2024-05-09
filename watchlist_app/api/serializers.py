from rest_framework import serializers
from watchlist_app.models import Movie


def is_capitalized(value):
    if value[0].islower():
        raise serializers.ValidationError('Value must be Capitalized!')


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        # All different ways to define fields
        exclude = ['active']
        # fields = '__all__'
        # fields = ['id', 'name', 'description']

    name_length = serializers.SerializerMethodField()

    # Name have to match the method field prefix by get_

    def get_name_length(self, object):
        return len(object.name)

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Name is too short!')
        if len(value) > 50:
            raise serializers.ValidationError('Name is too long!')
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Description is too short!')
        return value

    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError(
                'Name and Description should be different!')
        return data


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField(validators=[is_capitalized])
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate_name(self, value):
#         if len(value) < 3:
#             raise serializers.ValidationError('Name is too short!')
#         if len(value) > 50:
#             raise serializers.ValidationError('Name is too long!')
#         return value

#     def validate_description(self, value):
#         if len(value) < 10:
#             raise serializers.ValidationError('Description is too short!')
#         return value

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError(
#                 'Name and Description should be different!')
#         return data
