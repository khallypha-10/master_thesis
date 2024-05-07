from rest_framework import serializers
from . models import Patient, Doctor
from django.contrib.auth.models import User


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ['slug', 'user']
        lookup_field = 'slug'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ['slug', 'user']
        lookup_field = 'slug'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        lookup_field = 'username'