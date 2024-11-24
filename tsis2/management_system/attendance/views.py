from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Attendance
from .permissions import IsTeacherOrAdmin
from .serializers import AttendanceSerializer
from ..courses.models import Course
from ..students.models import Student


class AttendanceListView(APIView):
    def get(self, request):
        attendance_list = cache.get('attendance_list')
        if not attendance_list:
            queryset = Attendance.objects.all()
            attendance_list = AttendanceSerializer(queryset, many=True).data
            cache.set('attendance_list', attendance_list, timeout=300)
        return Response(attendance_list)


class MarkAttendanceView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        if not request.user == course.instructor and not request.user.is_staff:
            return Response({"detail": "You do not have permission to mark attendance for this course."},
                            status=status.HTTP_403_FORBIDDEN)

        student_ids = request.data.get("students", [])
        status_value = request.data.get("status", "Present")

        attendance_records = []
        for student_id in student_ids:
            student = get_object_or_404(Student, id=student_id)
            attendance = Attendance.objects.create(
                student=student,
                course=course,
                status=status_value
            )
            attendance_records.append(attendance)

        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, course_id):
        student = get_object_or_404(Student, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        attendance_records = Attendance.objects.filter(student=student, course=course)

        if attendance_records.exists():
            serializer = AttendanceSerializer(attendance_records, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "No attendance records found for this student in the specified course."},
                            status=status.HTTP_404_NOT_FOUND)
