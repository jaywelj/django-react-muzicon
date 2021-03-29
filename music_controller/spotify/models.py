from .credentials import (
    CLIENT_ID,
    CLIENT_SECRET,
)
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from requests import post


class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

    def is_spotify_authenticated(self):
        if self.expires_in <= timezone.now():
            return False
        return True

    def refresh_access_token(self):
        print(self.is_spotify_authenticated())
        if not self.is_spotify_authenticated():
            print("BITCH AUTHENTICATED!")
            response = post(
                "https://accounts.spotify.com/api/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                },
            ).json()
            print(response)
            self.access_token = response.get("access_token")
            self.save()
