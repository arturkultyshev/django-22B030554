"""
URL configuration for management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from courses.views import CourseListView
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from students.views import StudentListView

router = routers.DefaultRouter()
router.register(r'students', StudentListView)
router.register(r'courses', CourseListView)

schema_view = get_schema_view(
    openapi.Info(
        title="Student Management API",
        default_version='v1',
        description="API documentation for the Student Management System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@studentmanagement.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/students/', include('students.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/grades/', include('grades.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/notifications/', include('notifications.urls')),

    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/analytics/', include('analytics.urls')),
]
