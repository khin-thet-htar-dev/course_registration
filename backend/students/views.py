from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from .models import Student, Enrollment
from .serializers import StudentSerializer, EnrollmentSerializer
from backend.courses.models import Course

# Create your views here.

class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'student_id': ['exact', 'contains'],
            'name': ['exact', 'contains'],
            'email': ['exact', 'contains'],
            'enrollment_date': ['exact', 'gte', 'lte'],
        }

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_class = StudentFilter
    lookup_field = 'student_id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def courses(self, request, student_id=None):
        student = self.get_object()
        enrollments = student.enrollment_set.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(student_id=request.data['student_id'])
            course = Course.objects.get(id=request.data['course_id'])
            enrollment = Enrollment.objects.create(student=student, course=course)
            serializer = self.get_serializer(enrollment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (Student.DoesNotExist, Course.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)