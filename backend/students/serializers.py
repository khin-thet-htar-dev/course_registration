from rest_framework import serializers
from .models import Student, Enrollment
from backend.courses.serializers import CourseSerializer

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'name', 'email', 'enrollment_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    student_id = serializers.CharField(write_only=True)
    course_id = serializers.CharField(write_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'student_id', 'course_id', 'enrolled_date']
        read_only_fields = ['enrolled_date'] 