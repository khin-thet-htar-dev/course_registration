from rest_framework import serializers
from .models import Grade
from backend.students.serializers import StudentSerializer
from backend.courses.serializers import CourseSerializer

class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    student_id = serializers.CharField(write_only=True)
    course_id = serializers.CharField(write_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'student_id', 'course_id', 'grade', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 