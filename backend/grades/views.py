from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters import rest_framework as filters
import csv
import io
from .models import Grade
from .serializers import GradeSerializer
from backend.students.models import Student
from backend.courses.models import Course

class GradeFilter(filters.FilterSet):
    class Meta:
        model = Grade
        fields = {
            'grade': ['exact'],
            'student__name': ['exact', 'contains'],
            'course__course_name': ['exact', 'contains'],
            'created_at': ['gte', 'lte'],
        }

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filterset_class = GradeFilter
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(student_id=request.data['student_id'])
            course = Course.objects.get(id=request.data['course_id'])
            grade_data = {
                'student': student,
                'course': course,
                'grade': request.data['grade'],
                'comments': request.data.get('comments', '')
            }
            grade = Grade.objects.create(**grade_data)
            serializer = self.get_serializer(grade)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (Student.DoesNotExist, Course.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        csv_file = request.FILES['file']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        grades = []
        errors = []
        
        for row in reader:
            try:
                student = Student.objects.get(student_id=row['student_id'])
                course_id = request.data['course_id']
                course = Course.objects.get(id=course_id)
                
                grade_data = {
                    'student': student,
                    'course': course,
                    'grade': row['grade'],
                    'comments': row.get('comments', '')
                }

                
                grade = Grade.objects.create(**grade_data)
                serializer = self.get_serializer(grade)
                grades.append(serializer.data)
            except Exception as e:
                errors.append({
                    'row': row,
                    'error': str(e)
                })

        return Response({
            'grades': grades,
            'errors': errors
        }, status=status.HTTP_201_CREATED if not errors else status.HTTP_400_BAD_REQUEST)
