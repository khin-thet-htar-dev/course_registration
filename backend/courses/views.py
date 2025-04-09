from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from .models import Course
from .serializers import CourseSerializer
from backend.students.serializers import StudentSerializer
from backend.grades.serializers import GradeSerializer

# Create your views here.

class CourseFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            'course_id': ['exact', 'contains'],
            'course_name': ['exact', 'contains'],
            'instructor': ['exact', 'contains'],
            'semester': ['exact'],
        }

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter
    lookup_field = 'course_id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def students(self, request, course_id=None):
        course = self.get_object()
        students = course.student_set.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def grades(self, request, course_id=None):
        course = self.get_object()
        grades = course.grade_set.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)
