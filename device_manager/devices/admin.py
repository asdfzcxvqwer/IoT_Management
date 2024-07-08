from django.contrib import admin
from .models import Device, DeviceLog, DeviceOwnership

admin.site.register(DeviceLog)

class DeviceOwnershipInline(admin.TabularInline):
    model = DeviceOwnership

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    inlines = [
        DeviceOwnershipInline,
    ]
