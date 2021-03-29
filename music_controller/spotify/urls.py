from django.urls import path
from .views import (
    AuthURLView,
    CurrentSongView,
    IsAuthenticatedView,
    PauseSongView,
    PlaySongView,
    SkipSongView,
    spotify_callback
)
    

urlpatterns = (
    path('get-auth-url', AuthURLView.as_view()),
    path('redirect', spotify_callback),
    path('is-authenticated', IsAuthenticatedView.as_view()),
    path('current-song', CurrentSongView.as_view()),
    path('play', PlaySongView.as_view()),
    path('pause', PauseSongView.as_view()),
    path('skip', SkipSongView.as_view()),
)
