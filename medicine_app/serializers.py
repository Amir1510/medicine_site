from rest_framework import serializers
from medicine_app.models import *
from django.db.models.functions import Coalesce 
from django.db.models import OuterRef, Value, F, CharField

class DataSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        queryset=Plan.objects.all(), slug_field='username'
    )
    class Meta:
        model = Data
        fields = ['id', 'username', 'data', 'time']

class PlannedSerializer(serializers.ModelSerializer):
    time = serializers.CharField(source='data.time')
    data = serializers.CharField(source='data.data')
    id = serializers.IntegerField(source='data.id')
    class Meta:
        model = Plan
        fields = ['id','username', 'weight','group_of_blood', 'height', 'age','data', 'time',]
class IsStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUser
        fields = ['is_staff']