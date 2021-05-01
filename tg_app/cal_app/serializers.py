from rest_framework import serializers
from cal_app.models import User, CalendarEvent, ConferenceRoom

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'company', 'email')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalendarEvent
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConferenceRoom
        fields = '__all__'
