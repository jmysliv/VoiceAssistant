from django.urls import path
from event_api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('events/', views.EventList.as_view()),
    path('events/<int:pk>/', views.EventDetail.as_view()),
    path('tasks/', views.TaskList.as_view()),
    path('tasks/<int:pk>/', views.TaskDetail.as_view()),
    path('messages/', views.MessageList.as_view()),
    path('messages/<int:pk>/', views.MessageDetail.as_view()),
    path('inbox/', views.show_inbox),
    path('register/', views.create_user),
    path('auth/', obtain_auth_token, name='api_token_auth'),
]