from django.urls import path
from . import views

urlpatterns = [
    path('', views.goal_list, name='goal-list'),
    path('new/', views.goal_create, name='goal-create'),
    path('<int:pk>/update/', views.goal_update, name='goal-update'),
    path('<int:pk>/delete/', views.goal_delete, name='goal-delete'),
]