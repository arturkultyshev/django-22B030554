from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Custom logic for updating notification (e.g., mark as read)
        if 'is_read' in validated_data:
            instance.is_read = validated_data['is_read']
        return super().update(instance, validated_data)
