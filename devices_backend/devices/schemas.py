from ninja import ModelSchema, Schema
from ninja.orm import create_schema
from devices.models import GameCenterDevice, Refreshment, Refresh, Invoice, InvoiceDevice, CalcTime
from datetime import datetime


class Error(Schema):
    message: str


class RefreshmentSchema(ModelSchema):
    class Meta:
        model = Refreshment
        fields = ("id", "name", "type", "price")


class RefreshmentCreateSchema(Schema):
    name: str
    type: str
    price: str


class GameCenterDeviceSchema(ModelSchema):
    class Meta:
        model = GameCenterDevice
        fields = ('id', 'name')


class GGCreateSchema(Schema):
    name: str
    person_name: str | None = None
    invoice_type: str | None = None


class InvoiceSchema(ModelSchema):
    class Meta:
        model = Invoice
        fields = ('id', 'name')


class InvoiceCreateSchema(Schema):
    name: str


class InvoiceDeviceSchema(ModelSchema):
    invoice: InvoiceSchema
    device: GameCenterDeviceSchema

    class Meta:
        model = InvoiceDevice
        fields = ('id', 'invoice', 'device')


class InvoiceRefreshSchema(ModelSchema):
    invoice: InvoiceSchema | None = None
    refreshs: RefreshmentSchema | None = None

    class Meta:
        model = Refresh
        fields = ('invoice', 'refreshs', 'quantity')
