from django.urls import path

from . import views

urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='attendance-list'),
    path('mark/', views.MarkAttendanceView.as_view(), name='attendance-mark'),
    path('student/<int:student_id>/', views.StudentAttendanceView.as_view(), name='student-attendance'),
]