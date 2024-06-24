from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise ValidationError({'error': 'password not match'})

        username = self.validated_data['username']
        if (User.objects.filter(username=username).exists()):
            raise ValidationError({'error': 'username already exists'})

        email = self.validated_data['email']
        if (User.objects.filter(email=email).exists()):
            raise ValidationError({'error': 'email already exists'})

        account = User(username=username, email=email)
        account.set_password(password)
        account.save()
        return account
