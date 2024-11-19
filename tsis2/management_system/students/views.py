from rest_framework.viewsets import ModelViewSet
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsAdmin, IsTeacher, IsStudent


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdmin() or IsTeacher() or IsStudent()]
        return [IsAdmin() or IsTeacher()]

