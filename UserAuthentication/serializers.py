from dataclasses import field
from rest_framework import serializers
from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
from .models import Performance

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'fname', 'phone', 'grade', 'board', 'institute', 'approved',
                  'is_superuser', 'is_staff', 'websiteURL', 'instagramURL', 'telegramURL', 'youtubeURL', 'facebookURL')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # print(validated_data)
        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'], fname=validated_data['fname'], phone=validated_data['phone'], institute=validated_data['institute'], board=validated_data['board'],
                                        grade=validated_data['grade'],
                                        is_superuser=validated_data['is_superuser'], is_staff=validated_data['is_staff'], websiteURL=validated_data['websiteURL'], instagramURL=validated_data['instagramURL'], facebookURL=validated_data['facebookURL'], youtubeURL=validated_data['youtubeURL'], telegramURL=validated_data['telegramURL'])

        return user


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=255)
    role = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['email', 'password', 'role']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PerformanceSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField()
    room_id = serializers.IntegerField()
    class Meta:
        model = Performance
        fields = '__all__'