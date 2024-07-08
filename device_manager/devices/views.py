from typing import Any
from django.db.models.query import QuerySet
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views import View
from django.views.generic.list import ListView
from .models import Device, DeviceLog, DeviceOwnership
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class PutLog(View):
    def post(self, request: HttpRequest, *args, serial_number: str = None, **kwargs):
        dev: Device = get_object_or_404(Device, serial_number=serial_number)
        data = request.body.decode()
        log = DeviceLog(device=dev, data=data)
        log.save()
        return JsonResponse({"status": "ok"}, safe=False)

    def get(self, request: HttpRequest, *args, serial_number: str = None, **kwargs):
        dev: Device = get_object_or_404(Device, serial_number=serial_number)
        res = {"status": "ok"}
        res.update(model_to_dict(dev))
        return JsonResponse(res, safe=False)
    
class DeviceList(LoginRequiredMixin, ListView):
    # model = Device
    login_url = "users/login"

    def get_queryset(self) -> QuerySet[Any]:
        return DeviceOwnership.objects.filter(
            user=self.request.user, ownership_for__isnull=True
        ).select_related("device")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        result = super().get_context_data(**kwargs)
        result.update({"has_permission": isinstance(self.request.user, User)})
        return result
