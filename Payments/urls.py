from django.urls import path 
from . import views 
 
urlpatterns = [
    path('csrf', views.csrf, name="csrf"),
    path('invoicelist', views.invoice_list, name='invoicelist'),
    path('siglerecord/<int:pk>', views.payment_link, name="siglerecord"),
    path('user-invoice-payment/<int:pk>', views.checkout, name="user-invoice-payment"),
]