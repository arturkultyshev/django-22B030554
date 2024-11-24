from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from ..grades.models import Grade
from ..notifications.utils import create_notification
from ..students.models import Student


@shared_task
def daily_attendance_reminder():
    today = datetime.today().date()
    students = Student.objects.all()
    for student in students:
        subject = "Reminder: Mark your attendance!"
        message = f"Dear {student.name}, please mark your attendance for today, {today}."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student.user.email])

    return "Attendance reminder sent to students."


@shared_task
def grade_update_notification(grade_id):
    grade = Grade.objects.get(id=grade_id)
    subject = f"Grade Update for {grade.course.name}"
    message = f"Dear {grade.student.name}, your grade for {grade.course.name} has been updated to {grade.grade}."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [grade.student.user.email])
    create_notification(grade.student.user, subject, message)

    return "Grade update notification sent."


@shared_task
def weekly_grade_summary():
    students = Student.objects.all()
    for student in students:
        grades = Grade.objects.filter(student=student)
        grade_summary = "\n".join([f"{grade.course.name}: {grade.grade}" for grade in grades])

        subject = f"Your Weekly Grade Summary"
        message = f"Dear {student.name},\n\nHere is your weekly grade summary:\n\n{grade_summary}\n\nKeep up the good work!"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student.user.email])

    return "Weekly grade summary sent to students."
