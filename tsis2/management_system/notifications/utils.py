from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Notification


@shared_task
def send_async_notification_email(user_id, subject, message):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )


def create_notification(user, subject, message):
    notification = Notification.objects.create(
        user=user,
        subject=subject,
        message=message
    )
    # Отправляем уведомление асинхронно
    send_async_notification_email.delay(user.id, subject, message)
    return notification
