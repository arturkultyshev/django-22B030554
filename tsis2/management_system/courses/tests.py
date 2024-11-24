from courses.models import Course
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testteacher', password='testpassword')
        self.course = Course.objects.create(
            name="Mathematics 101",
            description="Basic Mathematics",
            instructor=self.user
        )

    def test_course_creation(self):
        course = self.course
        self.assertEqual(course.name, "Mathematics 101")
        self.assertEqual(course.instructor.username, "testteacher")

    def test_course_str_method(self):
        self.assertEqual(str(self.course), "Mathematics 101")


class CourseViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testteacher', password='testpassword')
        self.course = Course.objects.create(
            name="Mathematics 101",
            description="Basic Mathematics",
            instructor=self.user
        )

    def test_course_detail_view(self):
        self.client.login(username='testteacher', password='testpassword')
        response = self.client.get(f'/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Mathematics 101")


class CachingTest(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name="Test Course",
            description="Course Description",
            instructor=self.user
        )

    def test_cache_usage(self):
        response1 = self.client.get('/courses/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        cache.set('courses', response1.data)

        response2 = self.client.get('/courses/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data, response2.data)
