from warnings import filters
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from .models import Doctor,User,News,Date
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

class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['specialization', 'experience', 'location',
                  'clinic_name', 'cunsultation_fee', 'is_consultation_fee',
                  'avaible_today']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.avatar:
            representation['avatar'] = settings.BASE_URL + instance.avatar.url
        else:
            representation['avatar'] = None
        return representation


class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "avatar"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','role']

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password = serializers.CharField(write_only=True)


class DateSerializer(serializers.Serializer):
    user=UserSerializer()
    class Meta:
        model = Date
        fields=['id','user','doctor','date','time','status']

class BookingSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Date
        fields=['id','user','doctor','date','time','status']

