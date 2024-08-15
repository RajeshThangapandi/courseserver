# newapi/api/views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, CourseInstance
from .serializers import CourseSerializer, CourseInstanceSerializer
from pprint import pprint


@api_view(['GET', 'POST'])
def courses_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        course_data = [{'title': course.title, 'code': course.course_code} for course in courses]
        return Response(course_data)
    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def course_detail(request, course_code):
    try:
        course = Course.objects.get(course_code=course_code)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        course.delete()
        return Response({'message': 'Course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_course_instance(request):
    serializer = CourseInstanceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_course_instances(request, year, semester):
    instances = CourseInstance.objects.filter(year=year, semester=semester)
    unique_instances = []
    seen = set()
    
    for instance in instances:
        identifier = (instance.course_code, instance.year, instance.semester)
        if identifier not in seen:
            seen.add(identifier)
            unique_instances.append(instance)
    
    serializer = CourseInstanceSerializer(unique_instances, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_course_instance(request, year, semester, course_code):
    instances = CourseInstance.objects.filter(year=year, semester=semester)
    unique_instances = []
    seen = set()
    
    for instance in instances:
        identifier = (instance.course_code, instance.year, instance.semester)
        if identifier not in seen:
            seen.add(identifier)
            unique_instances.append(instance)
    
    serializer = CourseInstanceSerializer(unique_instances, many=True)
    storedata= serializer.data
    exists = any(instance['course_code'] == course_code for instance in storedata)

    if(not exists):
       return Response({'error': 'Course in this semester not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        
        # pprint(Course.objects.get(course_code=course_code))
        course = Course.objects.get(course_code=course_code)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CourseSerializer(course)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_course_instance(request, year, semester, course_code):
    # Filter to get all instances matching the criteria
    instances = CourseInstance.objects.filter(year=year, semester=semester, course_code=course_code)
    
    if not instances.exists():
        return Response({"error": "No CourseInstance found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)
    
    # Delete all matching instances
    instances.delete()
    return Response({"error": "Course Instance Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def manage_course_instances(request):
    if request.method == 'GET':
        # Retrieve all CourseInstance objects
        instances = CourseInstance.objects.all()
        serializer = CourseInstanceSerializer(instances, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = CourseInstanceSerializer(data=request.data)
        if serializer.is_valid():
            # Extract data for validation
            course_code = request.data.get('course_code')
            year = request.data.get('year')
            semester = request.data.get('semester')

            # Check if an instance with the same course_code, year, and semester already exists
            if CourseInstance.objects.filter(course_code__course_code=course_code, year=year, semester=semester).exists():
                return Response({"error": "A CourseInstance with this course_code, year, and semester already exists."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # If not, save the new instance
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)