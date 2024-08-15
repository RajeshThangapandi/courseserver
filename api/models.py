# newapi/api/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    course_id=models.IntegerField(
        validators=[
            MinValueValidator(100),    # Minimum value
            MaxValueValidator(150)     # Maximum value (assuming semesters are 1 or 2)
        ]
    ,)
    course_code = models.CharField(max_length=100,unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.course_code})"

class CourseInstance(models.Model):
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE,to_field='course_code',
        db_column='course_code')
    
    year = models.IntegerField()
    semester = models.IntegerField()


    def __str__(self):
        return f"{self.course_code} - {self.year} S{self.semester}"
