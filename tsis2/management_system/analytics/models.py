from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from ..courses.models import Course


class UserAPIRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]

    def __str__(self):
        return f"API Request by {self.user.username} at {self.timestamp}"


class CoursePopularity(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    last_viewed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.course.name} - {self.views} views"


class ActiveUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User {self.user.username} last active at {self.last_activity}"
