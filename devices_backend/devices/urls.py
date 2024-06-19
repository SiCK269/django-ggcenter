from django.urls import path, reverse_lazy
from . import views

app_name = 'gg'

urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='all'),
    path('invoice/<int:pk>', views.invoice_detail, name='invoice_detail'),
]