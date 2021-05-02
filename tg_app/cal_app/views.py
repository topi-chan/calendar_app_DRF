from django.http import HttpResponse
#from django.shortcuts import render
from cal_app.models import User, CalendarEvent, ConferenceRoom
from .serializers import UserSerializer, EventSerializer, RoomSerializer #NestedRoomSerializer
#from .serializers import  EventDayViewSerializer, LocationIdViewSerializer
from rest_framework import viewsets, filters, status, generics, views
from rest_framework import authentication, permissions, exceptions
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
import datetime


#TODO: another way of authentication for Events (different from get_queryset)
class EventUserPermission(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        current_event = request.__dict__
        print(current_event)
        if (CalendarEvent.objects.filter(owner=current_user)  |
                CalendarEvent.objects.filter(participant_list=current_user)):
            return request.user

# class EventUserAuthentication(authentication.BaseAuthentication):
# #     def authenticate(self, request):
# # #        pass
# #         # logged_user = request.user
# #         # if not logged_user:
# #         #     return None
# #         try:
# #             'x' == 'x'
# # #            User.CalendarEvent_set.filter(user=logged_user).exists()
# #         except:
# #             raise exceptions.AuthenticationFailed("Unauthorized access")
# #         return (None)
#     def authenticate(self, request):
#         username = request.GET.get("username")
#
#         if not username: # no username passed in request headers
#             return None # authentication did not succeed
#
#         try:
#             user = User.objects.get(username=username) # get the user
#         except User.DoesNotExist:
#             raise exceptions.AuthenticationFailed('No such user') # raise exception if user does not exist
#
#         return (user, None) # authentication successful





def index(request):
    response = """<html><body><p>This is the main page of the Cal App.</p><br>
    It's a simple RESTful API for managing calendar events and conference room
    availability. Each user have his/her default ​timezone​.</body></html>"""
    return HttpResponse(response)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    #TODO: if changed authentication permission_classes = (EventUserPermission,)
    serializer_class = EventSerializer
    #TODO: for alternate auth method queryset = CalendarEvent.objects.all()

    def get_queryset(self):
        user = self.request.user
        return (CalendarEvent.objects.filter(owner=user) |
        CalendarEvent.objects.filter(participant_list=user))

    def perform_create(self, serializer):
#        qs = User.objects.filter(email=participant_list)
        serializer.save(owner=self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = ConferenceRoom.objects.all()


class EventDayView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = CalendarEvent.objects.all()

#    permission_classes = (EventUserPermission,)
    # def get_queryset(self):
    #     user = self.request.user
    #     return (CalendarEvent.objects.filter(owner=user) |
    #             CalendarEvent.objects.filter(participant_list=user))

    def get(self, request, year, month, day):
        event = CalendarEvent.objects.filter(start_date__year=str(year),
                           start_date__month=month, start_date__day=day)
        user = self.request.user
        if event.filter(owner=user).exists() or event.filter(participant_list=user).exists():
            serializer = EventSerializer(event, many=True)
        else:
            serializer
        return Response(serializer.data)


class LocationIdView(generics.ListAPIView):
    queryset = ConferenceRoom.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, loc):
        location = ConferenceRoom.objects.filter(address=loc)
        serializer = RoomSerializer(location, many=True)
        return Response(serializer.data)


class EventAgendaView(generics.ListAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = EventSerializer

    def get(self, request, query):
        queryset2 = ConferenceRoom.objects.all()
        serializer2 = RoomSerializer(queryset2, many=True)
        if CalendarEvent.objects.filter(event_name=query).exists():
            event = CalendarEvent.objects.filter(event_name=query)
        elif CalendarEvent.objects.filter(meeting_agenda=query).exists():
            event = CalendarEvent.objects.filter(meeting_agenda=query)
        serializer = EventSerializer(event, many=True)
        Serializer_list = [serializer.data, serializer2.data]
        return Response(Serializer_list)
