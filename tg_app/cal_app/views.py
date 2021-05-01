from django.http import HttpResponse
from django.shortcuts import render
from cal_app.models import User, CalendarEvent, ConferenceRoom
from .serializers import UserSerializer, EventSerializer, RoomSerializer
from rest_framework import viewsets, status, generics, views, permissions


def index(request):
    "View function for home page of site."
    return render(request, 'index.html')

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = CalendarEvent.objects.all()

    def perform_create(self, serializer):
        current_user = User.objects.get(user=self.request.user)
        print(current_user.email)
        serializer.save(owner=current_user.company)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = ConferenceRoom.objects.all()
