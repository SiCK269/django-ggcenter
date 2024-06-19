import re

from django.db import models
from django_extensions.db.fields import AutoSlugField
from datetime import datetime, date, timedelta
from pydantic import BaseModel, ConfigDict
from django.shortcuts import get_object_or_404, reverse
from django_resized import ResizedImageField

class Logo(models.Model):
    name = models.CharField(max_length=200)
    img = ResizedImageField(size=[200, 200], null=True)

class Refreshment(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    img = ResizedImageField(size=[200, 200], null=True)
    price = models.FloatField()

    def __str__(self):
        return self.name

    def image_url(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url

class GameCenterDevice(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=200)

    total_time = ''

    def get_start_time(self):
        q = CalcTime.objects.filter(device=self.id)
        for i in q:
            if i.start_time:
                return i.start_time.strftime('%I:%M %p')
            else:
                return 'None'

    def get_end_time(self):
        q = CalcTime.objects.filter(device=self.id)
        for i in q:
            if i.endtime:
                return i.endtime.strftime('%I:%M %p')
            else:
                return 'None'

    def get_time_name(self):
        q = CalcTime.objects.filter(device=self.id)
        for i in q:
            return i.time_name


    def get_time_diff(self):
        q = CalcTime.objects.filter(device=self.id)
        for i in q:
            if not i.start_time:
                pass
            else:
                today = datetime.today()
                d_start = datetime.combine(today, i.start_time)
                c = datetime.now() - d_start
                total_seconds = int(c.total_seconds())
                hours, remainder = divmod(total_seconds, 60 * 60)
                minutes, seconds = divmod(remainder, 60)
                total = '{} hrs {} mins {} secs'.format(hours, minutes, seconds)
                if i.endtime:
                    d_end = datetime.combine(today, i.endtime)
                    if d_end <= datetime.now():
                        return "Done"
                    else:
                        return total
                else:
                    return total

    def __str__(self):
        return self.name


class Invoice(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    device = models.ManyToManyField(GameCenterDevice, through='InvoiceDevice', related_name="device_owned")
    refreshment = models.ManyToManyField(Refreshment, through='Refresh', related_name="refreshs_owned")
    name = models.CharField(max_length=200)
    TYPE_CHOICES = (
        ('واصل', 'واصل'),
        ('مفتوح', 'مفتوح'),
    )
    invoice_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='None', null=True)
    person_name = models.CharField(max_length=200, default="لا احد", null=True)


    def get_absolute_url(self):
        return reverse("gg:invoice_detail", kwargs={
            'pk': self.id
        })

    def get_device_id(self):
        q = InvoiceDevice.objects.get(invoice=self.id)
        return GameCenterDevice.objects.get(id=q.device.id).id

    def get_devices(self):
        q = InvoiceDevice.objects.filter(invoice=self.id)
        res = []
        for i in q:
            res.append(f"{i.device.name}")
        return ' '.join(res)

    def get_refreshs(self):
        res = []
        q = Refresh.objects.filter(invoice=self.id)
        for i in q:
            res.append(i.refreshs.name)
            res.append(str(i.quantity))
        return ' '.join(res)

    def get_total_dev(self):
        devices = InvoiceDevice.objects.filter(invoice=self.id)
        num = list(devices)
        total = []
        for i in range(len(num)):
             total.append(int(devices[i].get_time_price()))
        return sum(total)

    def get_total_ref(self):
        res = []
        q = Refresh.objects.filter(invoice=self.id)
        num = list(q)
        for i in range(len(num)):
            res.append(int(q[i].get_total_price()))
        return sum(res)

    def get_total(self):
        return self.get_total_dev() + self.get_total_ref()

    def __str__(self):
        return f"{self.name} | {self.get_refreshs()} | {self.get_devices()}"


class InvoiceDevice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(GameCenterDevice, on_delete=models.CASCADE, null=True)

    def get_min_elapsed(self):
        q = CalcTime.objects.filter(device=self.device)
        for i in q:
            if not i.start_time:
                pass
            else:
                today = datetime.today()
                d_start = datetime.combine(today, i.start_time)
                c = datetime.now() - d_start
                total_seconds = int(c.total_seconds())
                total = round(total_seconds / 60)

                if i.endtime:
                    d_end = datetime.combine(today, i.endtime)
                    if d_end <= datetime.now():
                        n = d_end - d_start
                        total_second = int(n.total_seconds())
                        return round(total_second / 60)
                    else:
                        return total
                else:
                    return total

    def get_time_price(self):
        ps5 = ['ps1', 'ps2']
        ps4 = ['ps3', 'ps4', 'ps5', 'ps6', 'ps7', 'ps8', 'ps9', 'ps10', 'ps11', 'ps12', 'ps13', 'ps14']
        pc = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', 'pc10', 'pc11', 'pc12']

        minutes = self.get_min_elapsed()

        if self.device.name in ps5:
            q = CalcTime.objects.get(device=self.device)
            if self.device.name == q.device.name:
                if q.time_name == "فردي":
                    in_min = 50
                    c = in_min * minutes
                    return f"{round(c)}"
                elif q.time_name == "زوجي":
                    in_min = 66.666
                    c = in_min * minutes
                    return f"{round(c)}"
            else:
                return None

        if self.device.name in pc:

            q = CalcTime.objects.get(device=self.device)
            if self.device.name == q.device.name:
                in_min = 33.333
                c = in_min * minutes
                return f"{round(c)}"
            else:
                return None

        if self.device.name in ps4:

            q = CalcTime.objects.get(device=self.device)
            if self.device.name == q.device.name:
                if q.time_name == "فردي":
                    in_min = 41.666
                    c = in_min * minutes
                    return f"{round(c)}"
                elif q.time_name == "زوجي":
                    in_min = 50
                    c = in_min * minutes
                    return f"{round(c)}"
            else:
                return None

        if self.device.name == "x1" or "x2":

            q = CalcTime.objects.get(device=self.device)
            if self.device.name == q.device.name:
                in_min = 50
                c = in_min * minutes
                return f"{round(c)}"
            else:
                return None

        else:
            return None


class CalcTime(models.Model):
    device = models.ForeignKey(GameCenterDevice, on_delete=models.CASCADE)
    CHOICES = (
        ('فردي', 'فردي'),
        ('زوجي', 'زوجي'),
    )
    time_name = models.CharField(max_length=100, choices=CHOICES, default='فردي')


    created_at = models.DateField(auto_now_add=True)
    start_time = models.TimeField(null=True, blank=True)
    endtime = models.TimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.device}"


class Refresh(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    refreshs = models.ForeignKey(Refreshment, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.refreshs} | {self.quantity}"

    def get_total_price(self):
        return self.refreshs.price * self.quantity