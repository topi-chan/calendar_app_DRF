from . import views
from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from .views import UserViewSet, EventViewSet, RoomViewSet, EventDayView
from .views import LocationIdView, EventAgendaView

urlpatterns = [
    path('', views.index, name='index')
]

router = DefaultRouter()
router.register(r'api/users', UserViewSet, basename='UserView')
router.register(r'api/events', EventViewSet, basename='EventView')
router.register(r'api/rooms', RoomViewSet, basename='RoomView')

urlpatterns += [
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework'))]

urlpatterns += [
    path(r'date=<int:year>-<int:month>-<int:day>', EventDayView.as_view()),
    path(r'location_id=<str:loc>', LocationIdView.as_view()),
    path(r'query=<str:query>', EventAgendaView.as_view())
    ]
