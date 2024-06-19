from django.contrib import admin
from devices.models import Invoice, InvoiceDevice, GameCenterDevice, Refreshment, CalcTime, Refresh, Logo

# Register your models here.
class CalcTimeAdmin(admin.ModelAdmin):
    readonly_fields = ('start_time',)

admin.site.register(Invoice)
admin.site.register(InvoiceDevice)
admin.site.register(GameCenterDevice)
admin.site.register(Refreshment)
admin.site.register(CalcTime, CalcTimeAdmin)
admin.site.register(Refresh)
admin.site.register(Logo)
