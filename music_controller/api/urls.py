from django.urls import path
from .views import (
    RoomLeaveView,
    RoomCreateView,
    RoomGetView,
    RoomJoinView,
    RoomView,
    RoomUpdateView,
    RedirectUserView,
)
    

urlpatterns = [
    path('rooms', RoomView.as_view()),
    path('create-room', RoomCreateView.as_view()),
    path('update-room', RoomUpdateView.as_view()),
    path('get-room', RoomGetView.as_view()),
    path('join-room', RoomJoinView.as_view()),
    path('leave-room', RoomLeaveView.as_view()),
    path('redirect-user', RedirectUserView.as_view()),
]
