import peewee
import uuid
from enum import Enum, unique
from .base import db


class GBDeviceModel(db.Model):
    class Meta:
        table_name = "gb_device"

    @unique
    class SocketType(Enum):
        UDP = 1
        TCP = 2

    id = peewee.UUIDField(
        primary_key=True, default=uuid.uuid4(), unique=True, help_text="主键ID"
    )
    device_id = peewee.CharField(max_length=255)
    device_name = peewee.CharField(max_length=255)
    device_domain = peewee.CharField(max_length=255)
    socket_type = peewee.SmallIntegerField(
        default=SocketType.UDP, help_text="1-UDP 2-TCP"
    )
