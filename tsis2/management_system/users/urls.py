from django.urls import path
from djoser import views as djoser_views

urlpatterns = [
    path('register/', djoser_views.UserCreate.as_view(), name='user-register'),
    path('login/', djoser_views.LoginView.as_view(), name='user-login'),
    path('logout/', djoser_views.LogoutView.as_view(), name='user-logout'),
    path('me/', djoser_views.UserViewSet.as_view(), name='user-me'),
]