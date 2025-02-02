from warnings import filters
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from .models import Doctor,User,News
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('first_name','last_name','avatar')

    def get_avatar(self, obj):
        if obj.avatar:
            return settings.BASE_URL + obj.avatar.url
        return None


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'specialization', 'experience', 'location',
                  'clinic_name', 'cunsultation_fee', 'is_consultation_fee',
                  'avaible_today']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if user_data:
            user_instance = instance.user
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        return instance

class NewsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    img=serializers.SerializerMethodField()
    class Meta:
        model = News
        fields=['user','title','img','created_at']

    def get_img(self,obj):
        if obj.img:
            return settings.BASE_URL + obj.img.url
        return None

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','role']

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password = serializers.CharField(write_only=True)