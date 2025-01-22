from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['specialization','experience','location','clinic_name','cunsultation_fee','is_consultation_fee','avaible_today']