from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'pk',
            'code',
            'host',
            'guest_can_pause',
            'votes_to_skip',
            'created',
        )


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'guest_can_pause',
            'votes_to_skip',
        )