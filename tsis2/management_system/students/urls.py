from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'students', views.StudentListView, basename='students')

urlpatterns = [
    path('', views.StudentListView.as_view(), name='student-list'),
    path('<int:id>/', views.StudentProfileView.as_view(), name='student-detail'),
]
