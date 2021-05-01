from django.db import models
from django.contrib.auth.models import AbstractUser
import pytz
from timezone_field import TimeZoneField


class User(AbstractUser):

    company = models.IntegerField(blank=True, default=0)
    timezone = TimeZoneField(default='Europe/London')

    def __str__(self):
        return self.email

class ConferenceRoom(models.Model):

    name = models.CharField(max_length=500, null=False)
    address = models.TextField(max_length=2000, null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class CalendarEvent(models.Model):

    event_name = models.CharField(max_length=1000, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    meeting_agenda = models.TextField(max_length=2000, null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    participant_list = models.TextField(blank=True)
    location = models.ForeignKey(ConferenceRoom, on_delete=models.SET_NULL,
                                 null=True)

    def __str__(self):
        return self.event_name
