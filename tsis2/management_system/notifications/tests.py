from unittest.mock import patch

from ..notifications.tasks import daily_attendance_reminder, grade_update_notification
from rest_framework.test import APITestCase


class CeleryTasksTest(APITestCase):
    @patch('notifications.tasks.send_mail')
    def test_daily_attendance_reminder(self, mock_send_mail):
        daily_attendance_reminder()
        mock_send_mail.assert_called_once_with(
            'Reminder: Mark your attendance!',
            'Dear Student, please mark your attendance for today, 2024-11-24.',
            'from@example.com',
            ['student@example.com']
        )

    @patch('notifications.tasks.send_mail')
    def test_grade_update_notification(self, mock_send_mail):
        grade_update_notification(1)
        mock_send_mail.assert_called_once_with(
            'Your grade has been updated!',
            'Dear Student, your grade for the course has been updated.',
            'from@example.com',
            ['student@example.com']
        )
