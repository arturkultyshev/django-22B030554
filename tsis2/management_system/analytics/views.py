from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAdminUser

from models import UserAPIRequest, CoursePopularity, ActiveUser


class UserAPIRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAPIRequest
        fields = '__all__'


class CoursePopularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePopularity
        fields = '__all__'


class ActiveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveUser
        fields = '__all__'


class UserAPIRequestViewSet(viewsets.ModelViewSet):
    queryset = UserAPIRequest.objects.all()
    serializer_class = UserAPIRequestSerializer
    permission_classes = [IsAdminUser]


class CoursePopularityViewSet(viewsets.ModelViewSet):
    queryset = CoursePopularity.objects.all()
    serializer_class = CoursePopularitySerializer
    permission_classes = [IsAdminUser]


class ActiveUserViewSet(viewsets.ModelViewSet):
    queryset = ActiveUser.objects.all()
    serializer_class = ActiveUserSerializer
    permission_classes = [IsAdminUser]
