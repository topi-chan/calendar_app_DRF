from django.http import HttpResponse
from cal_app.models import User, CalendarEvent, ConferenceRoom
from .serializers import UserSerializer, EventSerializer, RoomSerializer
from rest_framework import viewsets, filters, status, generics, views
#TODO: alternate auth method from rest_framework import authentication, permissions, exceptions
#TODO: from rest_framework.permissions import BasePermission
from rest_framework.response import Response
import datetime


def index(request):
    response = """<html><body><p>This is the main page of the Cal App.</p><br>
    It's a simple RESTful API for managing calendar events and conference room
    availability. Each user have his/her default ​timezone​.</body></html>"""
    return HttpResponse(response)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    #TODO: if changed authentication: permission_classes = (EventUserPermission,)
    serializer_class = EventSerializer
    #TODO: for alternate auth method: queryset = CalendarEvent.objects.all()

    def get_queryset(self):
        '''
        Authentication method: specifies how queryset is returned - hence which
        users can view which event objects.
        '''
        user = self.request.user
        return (CalendarEvent.objects.filter(owner=user) |
        CalendarEvent.objects.filter(participant_list=user))

    def perform_create(self, serializer):
        '''Ensures that event owner is always a currently logged user.'''
        serializer.save(owner=self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = ConferenceRoom.objects.all()


class EventDayView(generics.GenericAPIView):
    serializer_class = EventSerializer
    queryset = CalendarEvent.objects.all()

    def get(self, request, year, month, day):
        '''Returns a queryset by date values passed in the URL.'''
        event = CalendarEvent.objects.filter(start_date__year=str(year),
                           start_date__month=month, start_date__day=day)
        user = self.request.user
        if event.filter(owner=user).exists() or event.filter(participant_list
                                                              =user).exists():
            serializer = EventSerializer(event, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class LocationIdView(generics.GenericAPIView):
    queryset = ConferenceRoom.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, loc):
        '''Returns a queryset by event location value passed in the URL.'''
        location = ConferenceRoom.objects.filter(address=loc)
        serializer = RoomSerializer(location, many=True)
        return Response(serializer.data)


class EventAgendaView(generics.GenericAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = EventSerializer

    def get(self, request, query):
        '''
        Returns a queryset by event name or description value passed in the URL.
        '''
        queryset2 = ConferenceRoom.objects.all()
        serializer2 = RoomSerializer(queryset2, many=True)
        if CalendarEvent.objects.filter(event_name=query).exists():
            event = CalendarEvent.objects.filter(event_name=query)
        elif CalendarEvent.objects.filter(meeting_agenda=query).exists():
            event = CalendarEvent.objects.filter(meeting_agenda=query)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        if event.filter(owner=user).exists() or event.filter(participant_list
                                                              =user).exists():
            serializer = EventSerializer(event, many=True)
            Serializer_list = [serializer.data, serializer2.data]
            return Response(Serializer_list)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


#TODO: another way of authentication for Events (different from get_queryset)
# class EventUserPermission(BasePermission):
#     def has_permission(self, request, view):
#         current_user = request.user
#         current_event = request.__dict__
#         print(current_event)
#         if (CalendarEvent.objects.filter(owner=current_user)  |
#                 CalendarEvent.objects.filter(participant_list=current_user)):
#             return request.user
