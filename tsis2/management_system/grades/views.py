from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Grade
from .serializers import GradeSerializer
from ..courses.models import Course
from ..students.models import Student


class GradeListView(APIView):
    def get(self, request):
        grades = cache.get('grades_list')
        if not grades:
            queryset = Grade.objects.all()
            grades = GradeSerializer(queryset, many=True).data
            cache.set('grades_list', grades, timeout=300)
        return Response(grades)


class GradeDetailView(APIView):
    def get(self, request, pk):
        cache_key = f'grade_detail_{pk}'
        grade = cache.get(cache_key)
        if not grade:
            grade_obj = Grade.objects.filter(pk=pk).first()
            if not grade_obj:
                return Response({'error': 'Grade not found'}, status=404)
            grade = GradeSerializer(grade_obj).data
            cache.set(cache_key, grade, timeout=300)
        return Response(grade)


class GradeCreateView(APIView):

    def post(self, request, student_id, course_id):
        student = get_object_or_404(Student, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        grade, created = Grade.objects.get_or_create(student=student, course=course)

        if not created:
            grade.grade = request.data.get('grade', grade.grade)
            grade.save()
            return Response(
                {"message": f"Grade for student {student.name} updated in course {course.name}."},
                status=status.HTTP_200_OK,
            )

        grade.grade = request.data.get('grade')
        grade.save()

        return Response(
            {"message": f"Grade for student {student.name} added in course {course.name}."},
            status=status.HTTP_201_CREATED,
        )
