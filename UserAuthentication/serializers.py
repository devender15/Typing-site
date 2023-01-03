from dataclasses import field
from rest_framework import serializers
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'fname', 'phone', 'grade', 'board', 'institute', 'approved', 'is_superuser', 'is_staff', 'website_url', 'instagram_url', 'telegram_url', 'youtube_url', 'facebook_url')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    

    def create(self, validated_data):
        
        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'], fname=validated_data['fname'], phone=validated_data['phone'], institute=validated_data['institute'], board=validated_data['board'], 
        grade=validated_data['grade'],
        is_superuser=validated_data['is_superuser'], is_staff=validated_data['is_staff'], website_url=validated_data['websiteURL'], instagram_url=validated_data['instagramURL'], facebook_url=validated_data['facebookURL'], youtube_url=validated_data['youtubeURL'], telegram_url=validated_data['telegramURL'])

        return user


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=255)
    role =  serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['email', 'password', 'role']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'