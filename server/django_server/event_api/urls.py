from django.urls import path
from event_api import views

urlpatterns = [
    path('events/', views.events_list),
    path('events/<int:pk>/', views.event_details),
    path('tasks/', views.tasks_list),
    path('tasks/<int:pk>/', views.task_details),
]