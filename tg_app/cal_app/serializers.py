from rest_framework import serializers
from cal_app.models import User, CalendarEvent, ConferenceRoom

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
#    participant_list = serializers.ListField(child=serializers.EmailField())
#    participant_list = serializers.StringRelatedField(many=True)

    class Meta:
        model = CalendarEvent
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConferenceRoom
        fields = '__all__'


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
