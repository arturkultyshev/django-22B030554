from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course
from .serializers import CourseSerializer
from ..students.models import Student


class CourseListView(APIView):
    def get(self, request):
        courses = cache.get('courses_list')
        if not courses:
            queryset = Course.objects.all()
            courses = CourseSerializer(queryset, many=True).data
            cache.set('courses_list', courses, timeout=300)
        return Response(courses)


class CourseUpdateView(APIView):
    def put(self, request, pk):
        course = Course.objects.filter(pk=pk).first()
        if not course:
            return Response({'error': 'Course not found'}, status=404)

        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('courses_list')
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class CourseDetailView(APIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        # Retrieve the course by its ID
        course = self.get_object()
        serializer = self.get_serializer(course)
        return Response(serializer.data)


class EnrollStudentView(APIView):

    def post(self, request, student_id, course_id):
        # Retrieve the student and course by their respective IDs
        student = get_object_or_404(Student, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        # Assuming you have an Enrollment model to handle many-to-many relationship
        course.students.add(student)

        # Return a response indicating successful enrollment
        return Response(
            {"message": f"Student {student.name} enrolled in course {course.name}."},
            status=status.HTTP_201_CREATED,
        )
