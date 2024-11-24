from django.db import models


class Notification(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.subject}'
