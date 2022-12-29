from rest_framework import serializers
from .models import *

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exams
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = '__all__'
