from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import invoiceData


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = invoiceData
        fields = ('invoiceNumber',
                  'clientEmail',
                  'clientName',
                  'projectName',
                  'amout',
                  'paymentlink',
                  'id',
                  'paymentstatus')

