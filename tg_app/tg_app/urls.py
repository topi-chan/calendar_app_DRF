from django.contrib import admin
from django.urls import path
from django.urls import include
#bonus urls below
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cal_app.urls')),
]
