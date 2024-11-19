from celery import shared_task


@shared_task
def send_attendance_reminder():
    # Logic to send attendance reminders
    pass