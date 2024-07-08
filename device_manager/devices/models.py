import datetime
from django.db import models
from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    deletion,
    DateTimeField,
    TextField,
)
from django.contrib.auth.models import User

class Device(Model):
    serial_number = CharField(max_length=64, primary_key=True)
    model = CharField(max_length=64, blank=True)
    public_key = TextField(blank=True)
    current_owner = ForeignKey(User, deletion.CASCADE, null=True)

    @property
    def current_owner(self) -> User:
        current_ownership = self.ownership
        owner = None
        if current_ownership is not None:
            owner = current_ownership.user
        return owner

    @property
    def ownership(self):
        return DeviceOwnership.objects.filter(
            device=self, ownership_for__isnull=True
        ).first()

    def new_owner(self, owner: User):
        now = datetime.datetime.utcnow()
        current_ownership = self.ownership
        if current_ownership is not None:
            current_ownership.ownership_for = now
            current_ownership.save()

        new_ownership = DeviceOwnership(device=self, user=owner, ownership_since=now)
        new_ownership.save()
        self.current_owner = owner
        pass

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__} model {self.model} SN {self.serial_number} by {self.ownership.user.get_full_name()} as {self.ownership.device_name}"
            if self.ownership is not None
            else f"{self.model} {self.serial_number}"
        )

class DeviceOwnership(Model):
    device = ForeignKey(Device, deletion.CASCADE)
    device_name = CharField(max_length=64, blank=True)
    user = ForeignKey(User, deletion.CASCADE, null=True)
    ownership_since = DateTimeField(null=True, blank=True)
    ownership_for = DateTimeField(null=True, blank=True)
    banner = models.ImageField(default='default.png', blank=True)

class DeviceLog(Model):
    device = ForeignKey(Device, deletion.CASCADE)
    data = TextField(blank=True)