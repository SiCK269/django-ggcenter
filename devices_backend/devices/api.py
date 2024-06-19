from django.shortcuts import get_object_or_404
from ninja_extra import NinjaExtraAPI, api_controller, route, permissions, throttle
from devices.models import  GameCenterDevice, Refreshment, Refresh, Invoice, InvoiceDevice, CalcTime
from devices.schemas import (
    Error,
    GameCenterDeviceSchema,
    GGCreateSchema,
    InvoiceSchema,
    InvoiceCreateSchema,
    InvoiceDeviceSchema,
    InvoiceRefreshSchema,
)

app = NinjaExtraAPI()


@api_controller('/gg/devices', tags=['GGcenter'], permissions=[])
class GGCenterController:
    @route.get("/", response=list[GameCenterDeviceSchema])
    def get_devs(self):
        return GameCenterDevice.objects.all()

    @route.post("/", response=list[GameCenterDeviceSchema])
    def create_device(self, device: GGCreateSchema):
        device_data = device.model_dump()
        device_model = GameCenterDevice.objects.create(**device_data)
        return device_model


@api_controller('/gg', tags=['GGcenter'], permissions=[])
class InvoiceController:
    @route.get("/", response=list[InvoiceSchema])
    def get_devs(self):
        return Invoice.objects.all()

    @route.post("/", response=list[InvoiceSchema])
    def create_device(self, invoice_info: InvoiceCreateSchema):
        invoice_data = invoice_info.model_dump()
        invoice_model = Invoice.objects.create(**invoice_data)
        return invoice_model

    @route.get("/{id}/", response=InvoiceSchema)
    def get_invoice(self, id: int):
        invoice = get_object_or_404(Invoice, id=id)
        return invoice

    @route.get("/{id}/devices/", response=list[InvoiceDeviceSchema])
    def get_inv_device(self, id: int):
        return InvoiceDevice.objects.filter(invoice=id)


    @route.get("/{id}/refreshs", response=list[InvoiceRefreshSchema])
    def get_inv_refs(self, id: int):
        return Refresh.objects.filter(invoice=id)


@api_controller('/gg/inv_dev', tags=['GGcenter'], permissions=[])
class InvoiceDeviceController:
    @route.get("/", response=list[InvoiceDeviceSchema])
    def get_devs(self):
        return Invoice.objects.all()

    @route.get("/", response=InvoiceSchema)
    def get_invoice(self, id: int):
        inv_dev = get_object_or_404(InvoiceDevice, invoice=id)
        return inv_dev


app.register_controllers(
    InvoiceController,
)
