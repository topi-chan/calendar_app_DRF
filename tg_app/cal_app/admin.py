from django.contrib import admin
from .models import User, ConferenceRoom, CalendarEvent

admin.site.register(User)
admin.site.register(ConferenceRoom)
admin.site.register(CalendarEvent)
