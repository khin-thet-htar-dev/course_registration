from django.db import models
from django.core.validators import MinLengthValidator

class Course(models.Model):
    course_id = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(5)])
    course_name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_id} - {self.course_name}"

    class Meta:
        ordering = ['-created_at']
