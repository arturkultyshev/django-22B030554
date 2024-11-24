from rest_framework import serializers

from .models import Course, Enrollment


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor', 'instructor_name']
        read_only_fields = ['id', 'instructor_name']

    def validate_name(self, value):
        if Course.objects.filter(name=value).exists():
            raise serializers.ValidationError(f"Course with the name '{value}' already exists.")
        return value


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'student_name', 'course_name']
        read_only_fields = ['id', 'student_name', 'course_name']

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')

        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError(f"{student.get_full_name()} is already enrolled in {course.name}.")

        return data
