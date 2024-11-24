from rest_framework import serializers

from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'grade', 'date']
        read_only_fields = ['id', 'date']

    def validate_grade(self, value):
        valid_grades = ['A', 'B', 'C', 'D', 'F']
        if value not in valid_grades:
            raise serializers.ValidationError("Grade must be one of: 'A', 'B', 'C', 'D', 'F'.")
        return value
