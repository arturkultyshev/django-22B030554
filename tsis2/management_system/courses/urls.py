from django.urls import path

from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course-list'),
    path('<int:id>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('enroll/<int:student_id>/<int:course_id>/', views.EnrollStudentView.as_view(), name='enroll-student'),
]
