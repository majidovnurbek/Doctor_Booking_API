from rest_framework import serializers
from .models import Doctor,User,News
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','avatar')


class DoctorSerializer(serializers.ModelSerializer):
    user =  UserSerializer()
    class Meta:
        model = Doctor
        fields = ['user','specialization','experience','location','clinic_name','cunsultation_fee','is_consultation_fee','avaible_today']

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
