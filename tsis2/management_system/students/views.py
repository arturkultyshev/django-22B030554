from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Student
from .serializers import StudentSerializer


class StudentListView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of students.",
        responses={200: StudentSerializer(many=True)}
    )
    def get(self, request):
        students = cache.get('students_list')
        if not students:
            queryset = Student.objects.all()
            students = StudentSerializer(queryset, many=True).data
            cache.set('students_list', students, timeout=300)
        return Response(students)


class StudentProfileView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve a student's details.",
        responses={200: StudentSerializer}
    )
    def get(self, request, pk):
        cache_key = f'student_profile_{pk}'
        student_profile = cache.get(cache_key)
        if not student_profile:
            student = Student.objects.filter(pk=pk).first()
            if not student:
                return Response({'error': 'Student not found'}, status=404)
            student_profile = StudentSerializer(student).data
            cache.set(cache_key, student_profile, timeout=300)
        return Response(student_profile)
