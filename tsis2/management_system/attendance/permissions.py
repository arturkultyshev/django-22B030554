from rest_framework import permissions

from ..courses.models import Course


class IsTeacherOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        course_id = view.kwargs.get('course_id')
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                if request.user == course.instructor:
                    return True
            except Course.DoesNotExist:
                return False
        return False
