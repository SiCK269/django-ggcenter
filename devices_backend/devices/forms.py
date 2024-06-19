from django import forms
from .models import *


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'name', 'invoice_type'
        ]

class UpInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'name', 'invoice_type'
        ]


class DeviceForm(forms.ModelForm):
    class Meta:
        model = GameCenterDevice
        fields = [
            'name'
        ]


class RefreshUpdateForm(forms.ModelForm):
    class Meta:
        model = Refresh
        fields = [
            'quantity',
        ]


class RefreshAddForm(forms.ModelForm):
    class Meta:
        model = Refresh
        fields = [
            'refreshs', 'quantity',
        ]


class InvDeviceForm(forms.ModelForm):
    class Meta:
        model = InvoiceDevice
        fields = [
            'invoice', 'device',
        ]


class DevStart(forms.ModelForm):
    class Meta:
        model = CalcTime
        fields = [
            'time_name',
        ]


class DevUpdateTime(forms.ModelForm):
    class Meta:
        model = CalcTime
        fields = [
            'time_name',
        ]
