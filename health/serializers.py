from rest_framework import serializers
from .models import HealthProgram, Client, ClientEnrollment

class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    program = HealthProgramSerializer(read_only=True)
    
    class Meta:
        model = ClientEnrollment
        fields = '__all__'

class ClientDetailSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'