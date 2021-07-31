import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from Payments.models import invoiceData
from Payments.serializers import InvoiceSerializer

# initialize the APIClient app
client = Client()
# Create your tests here.


class InvoiceDataTest(TestCase):
    """ Test module for invoiceData model """
    def setUp(self):
        # Inserting a new record
        invoiceData.objects.create(
            invoiceNumber='WERT567TY', clientEmail='DRC@gmail.com', clientName='DRC', projectName='DRC Corporate',
            amout=20000, paymentlink='')

    def test_invoice_number(self):
        # verifying the record is created
        invoice = invoiceData.objects.get(invoiceNumber='WERT567TY')
        self.assertEqual(
            invoice.invoiceNumber, "WERT567TY")


class GetURLTests(TestCase):
    """ Testing the invoice list url which return all the invoice records """
    def test_testinginvoicegetrequest(self):
        response = self.client.get('/api/invoicelist')
        self.assertEqual(response.status_code, 200)

    def test_allinvoicedata(self):
        response = client.get(reverse('invoicelist'))
        invoice = invoiceData.objects.all()
        serializer = InvoiceSerializer(invoice, many=True)
        self.assertEqual(response.data, serializer.data)


class DeleteSingleInvoiceTest(TestCase):
    """ Test module for deleting an existing puppy record """

    def setUp(self):
        self.invoice = invoiceData.objects.create(
            invoiceNumber='TYUOPT567TY', clientEmail='KLC@gmail.com', clientName='HYUO', projectName='KOPU Corporate',
            amout=560000, paymentlink='')

    def test_valid_delete_invoice(self):
        response = client.delete(
            reverse('siglerecord', kwargs={'pk': self.invoice.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)







