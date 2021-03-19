from .models import Room
from .serializers import (
    RoomCreateUpdateSerializer,
    RoomSerializer,
)

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomJoinView(APIView):

    def post(self, request, format=None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        
        code = request.data.get('code')
        print(code)
        if code:
            room = Room.objects.filter(code=code).first()
            if room:
                request.session['room_code'] = code
                return Response(
                    {'meesage': "Room Joined"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'Bad Request': "Room not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {'Bad Request': "Missing required code key"},
            status=status.HTTP_400_BAD_REQUEST
        )


class RoomCreateView(APIView):
    serializer_class = RoomCreateUpdateSerializer

    def post(self, request, format=None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset.first()
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(
                    update_fields=(
                        "guest_can_pause",
                        "votes_to_skip",
                    )
                )
                self.request.session['room_code'] = room.code

                return Response(
                    RoomSerializer(room).data,
                    status=status.HTTP_200_OK,
                )
            else:
                room = Room(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip,
                )
                room.save()
                self.request.session['room_code'] = room.code
        
                return Response(
                    RoomSerializer(room).data,
                    status=status.HTTP_201_CREATED,
                )


class RoomGetView(APIView):
    serializer_class = RoomSerializer
    url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.url_kwarg)
        if code:
            room = Room.objects.filter(code=code).first()
            if room:
                data = self.serializer_class(room).data
                is_host = self.request.session.session_key == room.host
                data['is_host'] = is_host
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"Room Not Found": "Invalid room code."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"Bad Request": "Code parameter not found in request."},
            status=status.HTTP_404_NOT_FOUND,
        )


class RedirectUserView(APIView):

    def get(self, request, format=None):
        if not request.session.exists(request.session.session_key):
            request.session.create()

        data = {
            "code": request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


class RoomLeaveView(APIView):

    def post(self, request, format=None):
        message = "Left the Room"
        if "room_code" in self.request.session:
            self.request.session.pop("room_code")
            host = self.request.session.session_key
            room = Room.objects.filter(host=host).first()
            if room:
                room.delete()
                message = "Room Closed"

        return Response(
            {"Message": message},
            status=status.HTTP_200_OK,
        )


class RoomUpdateView(APIView):
    serializer_class = RoomCreateUpdateSerializer

    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = request.data.get('room_code')

            room = Room.objects.filter(code=code).first()
            if room:
                user_id = self.request.session.session_key
                if room.host == user_id:
                    room.guest_can_pause = guest_can_pause
                    room.votes_to_skip = votes_to_skip
                    room.save(
                        update_fields=(
                            "guest_can_pause",
                            "votes_to_skip",
                        )
                    )
                    return Response(
                        RoomSerializer(room).data,
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"FORBIDDEN": "You are not the host in this room",},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                return Response(
                    {"NOT FOUND": "Room not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"BAD REQUEST": "Invalid data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

                 