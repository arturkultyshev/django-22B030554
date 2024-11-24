from models import UserAPIRequest
from rest_framework.throttling import UserRateThrottle


class CustomUserRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        response = super().allow_request(request, view)
        if response:
            UserAPIRequest.objects.create(
                user=request.user,
                endpoint=request.path,
            )
        return response
