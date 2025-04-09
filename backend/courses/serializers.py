from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_id', 'course_name', 'instructor', 'semester', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 