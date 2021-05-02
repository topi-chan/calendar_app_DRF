from django.contrib import admin
from .models import User, ConferenceRoom, CalendarEvent


class EventAdmin(admin.ModelAdmin):
    '''Allows a convenient user event assigment in the Django admin panel.'''
    model = CalendarEvent
    filter_horizontal = ('participant_list',)

admin.site.register(User)
admin.site.register(ConferenceRoom)
admin.site.register(CalendarEvent, EventAdmin)
