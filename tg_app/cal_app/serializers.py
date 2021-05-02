from rest_framework import serializers
from cal_app.models import User, CalendarEvent, ConferenceRoom
from datetime import timedelta
#import datetime
import pytz


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    def get_date_joined(self, instance):
        '''Converts user join time value into logged user time zone.'''
        user = self.context.get('request').user
        date_with_timezone = instance.date_joined.astimezone(user.timezone)
        return date_with_timezone

    def get_last_login(self, instance):
        '''
        Converts user join time value into logged user time zone.
        If user never logged in returns None.
        '''
        if instance.last_login is None:
            return None
        user = self.context.get('request').user
        date_with_timezone = instance.last_login.astimezone(user.timezone)
        return date_with_timezone

    class Meta:
        '''Timezone field is excluded as it's not Json convertible.'''
        model = User
        exclude = ('timezone',)


class EventSerializer(serializers.ModelSerializer):
#    participant_list = serializers.ListField(child=serializers.EmailField())
#    participant_list = serializers.StringRelatedField(many=True)
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    def validate(self, data):
        '''Validates that event time doesn't exceed 8 hours.'''
        time_difference = data['end_date'] - data['start_date']
        time_difference_in_minutes = time_difference / timedelta(minutes=1)
        if time_difference_in_minutes > 480:
            raise serializers.ValidationError("Event time limit exceeded")
        return data

    def get_start_date(self, instance):
        '''
        Converts event start time value into logged user time zone.
        If empty returns None.
        '''
        if instance.start_date is None:
            return None
        user = self.context.get('request').user
        date_with_timezone = instance.start_date.astimezone(user.timezone)
        return date_with_timezone

    def get_end_date(self, instance):
        '''
        Converts event end time value into logged user time zone.
        If empty returns None.
        '''
        if instance.end_date is None:
            return None
        user = self.context.get('request').user
        date_with_timezone = instance.end_date.astimezone(user.timezone)
        return date_with_timezone

    class Meta:
        model = CalendarEvent
        fields = '__all__'



#data['description'],
#             owner = self.context['request']


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConferenceRoom
        fields = '__all__'


# class NestedRoomSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ConferenceRoom
#         fields = '__all__'
#        depth = 1

# class EventDayViewSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = CalendarEvent
#         fields = '__all__'
#
#
# class LocationIdViewSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ConferenceRoom
#         fields = '__all__'
# # for timezone check
# class MovieSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = '__all__'
#
#     def validate_rating(self, value):
#         if value < 1 or value > 10:
#             raise serializers.ValidationError('Rating has to be between 1 and 10.')
#         return value
