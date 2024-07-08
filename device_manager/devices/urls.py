from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from devices.views import PutLog, DeviceList

app_name = 'devices'

urlpatterns = [
    path('', DeviceList.as_view(), name='list'),
    path("put_log/<str:serial_number>/", csrf_exempt(PutLog.as_view()), name='put_log'),
]