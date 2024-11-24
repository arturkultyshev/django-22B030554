from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from ..students.models import Student


class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='testpassword')
        self.student = Student.objects.create(
            user=self.user,
            name="John Doe",
            email="john@example.com",
            dob="2000-01-01",
            registration_date="2023-01-01"
        )

    def test_student_creation(self):
        student = self.student
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(student.email, "john@example.com")
        self.assertEqual(student.user.username, "teststudent")

    def test_student_str_method(self):
        self.assertEqual(str(self.student), "John Doe")


class StudentViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='testpassword')
        self.student = Student.objects.create(
            user=self.user,
            name="John Doe",
            email="john@example.com",
            dob="2000-01-01",
            registration_date="2023-01-01"
        )

    def test_student_detail_view(self):
        self.client.login(username='teststudent', password='testpassword')
        response = self.client.get(f'/students/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "John Doe")


class StudentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='testpassword')
        self.student = Student.objects.create(
            user=self.user,
            name="John Doe",
            email="john@example.com",
            dob="2000-01-01",
            registration_date="2023-01-01"
        )

    def test_create_student(self):
        data = {'name': 'Jane Doe', 'email': 'jane@example.com', 'dob': '2001-01-01'}
        self.client.login(username='teststudent', password='testpassword')
        response = self.client.post('/students/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_student(self):
        data = {'name': 'Johnathan Doe'}
        self.client.login(username='teststudent', password='testpassword')
        response = self.client.patch(f'/students/{self.student.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Johnathan Doe')

    def test_delete_student(self):
        self.client.login(username='teststudent', password='testpassword')
        response = self.client.delete(f'/students/{self.student.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class StudentPermissionsTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='adminpassword')
        self.teacher = User.objects.create_user(username='teacher', password='teacherpassword')
        self.student = User.objects.create_user(username='student', password='studentpassword')

        self.student_instance = Student.objects.create(
            user=self.student,
            name="Student One",
            email="student1@example.com",
            dob="2000-01-01",
            registration_date="2023-01-01"
        )

    def test_student_can_access_their_own_data(self):
        self.client.login(username='student', password='studentpassword')
        response = self.client.get(f'/students/{self.student_instance.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_cannot_access_student_data(self):
        self.client.login(username='teacher', password='teacherpassword')
        response = self.client.get(f'/students/{self.student_instance.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_any_student_data(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(f'/students/{self.student_instance.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
