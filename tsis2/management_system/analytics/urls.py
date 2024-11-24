from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'api-requests', views.UserAPIRequestViewSet)
router.register(r'course-popularity', views.CoursePopularityViewSet)
router.register(r'active-users', views.ActiveUserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
