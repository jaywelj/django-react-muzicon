from .credentials import (
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
)
from .models import SpotifyToken
from .utils import execute_spotify_api_request
from api.models import Room
from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from requests import (
    Request, post, put,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AuthURLView(APIView):

    def get(self, request, format=None):
        scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

        url = Request(
            "GET",
            "https://accounts.spotify.com/authorize",
            params={
                "scope": scope,
                "response_type": "code",
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
            }
        ).prepare().url

        return Response({"url": url}, status=status.HTTP_200_OK)


class IsAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = request.session.session_key
        spotify_token = SpotifyToken.objects.filter(user=user)
        print(spotify_token)
        if spotify_token.exists():
            spotify_token.first().refresh_access_token()
        return Response(
            {"status": spotify_token.exists()},
            status=status.HTTP_200_OK
        )


class CurrentSongView(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code).first()
        if room:
            host = room.host
            endpoint = "player/currently-playing"
            spotify_token = SpotifyToken.objects.filter(user=host).first()
            response = execute_spotify_api_request(
                spotify_token,
                endpoint
            )
            if "error" in response or "item" not in response:
                return Response(
                    {},
                    status=status.HTTP_204_NO_CONTENT,
                )

            item = response.get("item")

            artist_string = ""
            for i, artist in enumerate(item.get("artists")):
                if i > 0:
                    artist_string += ", "
                artist_string += artist.get("name")

            song = {
                "title": item.get("name"),
                "artist": artist_string,
                "duration": item.get("duration_ms"),
                "time": response.get("progress_ms"),
                "image_url": item.get("album").get("images")[0].get("url"),
                "is_playing": response.get("is_playing"),
                "votes": 0,
                "id": item.get("id"),
            }

            return Response(
                song, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"Room Not Found": "You are not inside any room"}, status=status.HTTP_404_NOT_FOUND
            )


class PauseSongView(APIView):

    def put(self, response, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code).first()
        if self.request.session.session_key == room.host or room.guest_can_pause:
            spotify_token = SpotifyToken.objects.filter(user=room.host).first()
            execute_spotify_api_request(spotify_token, "player/pause",  is_put=True)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class PlaySongView(APIView):

    def put(self, response, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code).first()
        if self.request.session.session_key == room.host or room.guest_can_play:
            spotify_token = SpotifyToken.objects.filter(user=room.host).first()
            execute_spotify_api_request(spotify_token, "player/play",  is_put=True)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_403_FORBIDDEN)
    

class SkipSongView(APIView):

    def post(self, response, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code).first()
        if self.request.session.session_key == room.host:
            spotify_token = SpotifyToken.objects.filter(user=room.host).first()
            execute_spotify_api_request(spotify_token, "player/next",  is_post=True)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


def spotify_callback(request, format=None):
    code = request.GET.get("code")
    error = request.GET.get("error")

    response = post('https://accounts.spotify.com/api/token', data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }).json()
    access_token = response.get("access_token")
    token_type = response.get("token_type")
    refresh_token = response.get("refresh_token")
    expires_in = timezone.now() + timedelta(
        seconds=response.get("expires_in")
    )
    error = response.get("error")

    if not request.session.exists(request.session.session_key):
        request.session.create()

    spotify_token, is_created = SpotifyToken.objects.update_or_create(
        user=request.session.session_key,
        defaults={
            "token_type": token_type,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
        },
    )

    return redirect("frontend:")
