from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    def get(self, request):
        notifications = cache.get('notifications_list')
        if not notifications:
            queryset = Notification.objects.all()
            notifications = NotificationSerializer(queryset, many=True).data
            cache.set('notifications_list', notifications, timeout=300)
        return Response(notifications)


class SendNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Sends a notification to a user.
        Expects user ID and message in the request data.
        """
        user_id = request.data.get('user_id')
        message = request.data.get('message')

        if not user_id or not message:
            return Response({'detail': 'User ID and message are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the user based on the provided user ID
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Create the notification
        notification = Notification.objects.create(user=user, message=message)

        # Serialize the notification to return it in the response
        serializer = NotificationSerializer(notification)

        # Respond with the serialized notification
        return Response(serializer.data, status=status.HTTP_201_CREATED)
