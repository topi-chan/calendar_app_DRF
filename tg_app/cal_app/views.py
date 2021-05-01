from django.http import HttpResponse
from django.shortcuts import render
from cal_app.models import User, CalendarEvent, ConferenceRoom
from .serializers import UserSerializer, EventSerializer, RoomSerializer
#from .serializers import  EventDayViewSerializer, LocationIdViewSerializer
from rest_framework import viewsets, filters, status, generics, views, permissions
from rest_framework.response import Response
import datetime

def index(request):
    "View function for home page of the site."
    return render(request, 'index.html')


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = CalendarEvent.objects.all()

    def perform_create(self, serializer):
#        qs = User.objects.filter(email=participant_list)
        serializer.save(owner=self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = ConferenceRoom.objects.all()


class EventDayView(generics.ListAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = EventSerializer

    def get(self, request, year, month, day):
        event = CalendarEvent.objects.get(start_date__year=str(year),
                        start_date__month=month, start_date__day=day)
        serializer = EventSerializer(event)
        return Response(serializer.data)


class LocationIdView(generics.ListAPIView):
    queryset = ConferenceRoom.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, loc):
        location = ConferenceRoom.objects.get(address=loc)
        serializer = RoomSerializer(location)
        return Response(serializer.data)


class EventAgendaView(generics.ListAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = EventSerializer

    def get(self, request, query):
        if CalendarEvent.objects.filter(event_name=query).exists():
            event = CalendarEvent.objects.get(event_name=query)
        elif CalendarEvent.objects.filter(meeting_agenda=query).exists():
            event = CalendarEvent.objects.get(meeting_agenda=query)
        serializer = EventSerializer(event)
        return Response(serializer.data)
