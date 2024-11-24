from django.urls import path

from . import views

urlpatterns = [
    path('', views.GradeListView.as_view(), name='grade-list'),
    path('<int:id>/', views.GradeDetailView.as_view(), name='grade-detail'),
    path('add/', views.GradeCreateView.as_view(), name='grade-add'),
]
