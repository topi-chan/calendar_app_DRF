from . import views
from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, EventViewSet, RoomViewSet, EventDayView
from .views import LocationIdView, EventAgendaView

urlpatterns = [
    path('', views.index, name='index')]

router = DefaultRouter()
router.register(r'api/users', UserViewSet, basename='UserView')
router.register(r'api/events', EventViewSet, basename='EventView')
router.register(r'api/rooms', RoomViewSet, basename='RoomView')

urlpatterns += [
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework'))]

'''
Retrive date value as: YYYY-MM(M)-DD(D) with single digits as months / days.
Event location and query search is returned by descriptive string value.
'''
urlpatterns += [
    path(r'date=<int:year>-<int:month>-<int:day>', EventDayView.as_view()),
    path(r'location_id=<str:loc>', LocationIdView.as_view()),
    path(r'query=<str:query>', EventAgendaView.as_view())]
