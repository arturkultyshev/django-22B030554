from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import CustomUserSerializer


class UserListView(APIView):
    def get(self, request):
        users = cache.get('users_list')
        if not users:
            queryset = CustomUser.objects.all()
            users = CustomUserSerializer(queryset, many=True).data
            cache.set('users_list', users, timeout=300)
        return Response(users)


class UserUpdateView(APIView):
    def put(self, request, pk):
        user = CustomUser.objects.filter(pk=pk).first()
        if not user:
            return Response({'error': 'User not found'}, status=404)

        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('users_list')
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
