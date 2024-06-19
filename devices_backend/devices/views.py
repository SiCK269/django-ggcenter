from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View, generic
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import DeviceForm, RefreshAddForm, RefreshUpdateForm, InvoiceForm, DevStart, DevUpdateTime

from django.contrib import messages


# Create your views here.

class InvoiceListView(generic.FormView):
    template_name = "devices/invoice_list.html"
    form_class = InvoiceForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        invoices = Invoice.objects.all()
        invoice_device = InvoiceDevice.objects.all()
        refreshment = Refresh.objects.all()
        logo = Logo.objects.all()

        context["invoices"] = invoices
        context["invoice_devices"] = invoice_device
        context["refresh"] = refreshment
        context["logo"] = logo
        context["form"] = InvoiceForm

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        # form.send_email()
        # print "form is valid"
        return super(InvoiceListView, self).form_valid(form)


def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice_detail = InvoiceDevice.objects.filter(invoice=invoice.id)
    refreshments = Refreshment.objects.all()
    invoice_refresh = Refresh.objects.filter(invoice=invoice.id)
    logo = Logo.objects.all()

    if request.method == "POST":
        form = DeviceForm(request.POST)
        form2 = RefreshAddForm(request.POST)
        form3 = RefreshUpdateForm(request.POST)
        form4 = DevStart(request.POST)
        form5 = DevUpdateTime(request.POST)

        if "adddev" in request.POST:
            form = DeviceForm(request.POST)
            if form.is_valid():
                form.save()

                dev = GameCenterDevice.objects.latest('id')

                InvoiceDevice.objects.create(invoice=invoice, device=dev)

                return redirect('gg:invoice_detail', pk=pk)

        if "addref" in request.POST:
            form2 = RefreshAddForm(request.POST)

            refreshment = Refreshment.objects.get(name=request.POST.get('refreshs'))
            quantity = request.POST.get('quantity')

            ref = Refresh.objects.filter(invoice=invoice, refreshs=refreshment)

            if ref.exists():
                prev_quantity = ref[0].quantity
                ref.update(quantity=int(quantity) + prev_quantity)
            else:
                Refresh.objects.create(invoice=invoice, refreshs=refreshment, quantity=1)

            return redirect('gg:invoice_detail', pk=pk)

        if "upref" in request.POST:
            form3 = RefreshUpdateForm(request.POST)

            if form3.is_valid():
                refresh_up = form3.save(commit=False)
                refresh = Refreshment.objects.get(name=request.POST.get('name'))
                refresh_up.invoice = invoice
                refresh_up.name = refresh
                refresh_up.quantity = request.POST.get('quantity')

                Refresh.objects.filter(invoice=invoice, refreshs=refresh).update(quantity=request.POST.get('quantity'))

                return redirect('gg:invoice_detail', pk=pk)

        if 'startbtn' in request.POST:
            form4 = DevStart(request.POST)
            
            if form4.is_valid():
                time_type = request.POST.get('time_name')
                start = request.POST.get('start')
                device = GameCenterDevice.objects.get(id=request.POST.get('device'))


                get_time = CalcTime.objects.filter(device=device)
                if get_time.exists():
                    get_time.update(time_name=time_type, start_time=start)
                else:
                    CalcTime.objects.create(device=device, time_name=time_type, start_time=start)

                return redirect('gg:invoice_detail', pk=pk)

        if 'endbtn' in request.POST:
            form5 = DevUpdateTime(request.POST)

            if form5.is_valid():
                device = GameCenterDevice.objects.get(id=request.POST.get('device'))
                time_type = request.POST.get('time_name')
                start = datetime.strptime(request.POST.get('start'), "%I:%M %p")

                endtime = request.POST.get('end')

                get_endtime = CalcTime.objects.filter(device=device, time_name=time_type, start_time=start)

                if get_endtime.exists():
                    get_endtime.update(endtime=endtime)
                else:
                    CalcTime.objects.create(device=device, time_name=time_type, start_time=start, endtime=endtime)

                return redirect('gg:invoice_detail', pk=pk)

        if 'deletebtn' in request.POST:
            GameCenterDevice.objects.filter(id=request.POST.get('id')).delete()

            return redirect('gg:invoice_detail', pk=pk)
        
        if 'deleteref' in request.POST:
            ref_name = Refreshment.objects.get(name=request.POST.get('ref_name'))
            ref = Refresh.objects.filter(invoice=invoice, refreshs=ref_name)
            ref.delete()
            
            return redirect('gg:invoice_detail', pk=pk)

        if 'reset' in request.POST:
            Refresh.objects.filter(invoice=invoice).delete()
            invoice_dev = InvoiceDevice.objects.filter(invoice=invoice)
            for dev in invoice_dev:
                GameCenterDevice.objects.filter(id=dev.device.id).delete()
            invoice_dev.delete()

            return redirect('gg:invoice_detail', pk=pk)

        if 'deleteinv' in request.POST:
            Refresh.objects.filter(invoice=invoice).delete()
            invoice_dev = InvoiceDevice.objects.filter(invoice=invoice)
            for dev in invoice_dev:
                GameCenterDevice.objects.filter(id=dev.device.id).delete()
            invoice_dev.delete()
            Invoice.objects.filter(id=invoice.id).delete()

            return redirect('gg:all')

    else:
        form = DeviceForm()
        form2 = RefreshAddForm()
        form3 = RefreshUpdateForm()
        form4 = DevStart()
        form5 = DevUpdateTime()

    return render(request, 'devices/invoice_detail.html',
                  context={'invoice': invoice, "invoice_devices": invoice_detail, "refresh": invoice_refresh, "refreshments": refreshments, 'logo': logo,
                           'dev_form': form, 'ref_form': form2, 'ref_upd': form3, 'dev_start': form4, 'dev_end': form5, 'datetime': datetime})
