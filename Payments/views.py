# from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from Payments.serializers import InvoiceSerializer
from rest_framework.decorators import api_view
from Payments.models import invoiceData

from urllib.parse import urlencode
import contextlib
from urllib.request import urlopen

from django.conf import  settings
import stripe
from django.middleware.csrf import get_token
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


def csrf(request):
    print(get_token(request))
    return JsonResponse({'csrfToken': get_token(request)})


def make_shorten(url):
    """
    It is user defined function to shorten the payment link URL
    param: url : original payment link
    return : shorten ulr
    """
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url': url}))
    with contextlib.closing(urlopen(request_url)) as response:
        result = response.read().decode('utf-8')
        return result


@api_view(['GET', 'POST'])
def invoice_list(request):
    """
    API View for listing invoice data, inserting new invoice and delete existing invoice record
    :param request: Http Request object
    :return: it return 
    """
    try:
        if request.method == 'GET':
            # return list of all invoice records
            invoice = invoiceData.objects.all()
            invoice_serializer = InvoiceSerializer(invoice, many=True)
            return Response(invoice_serializer.data)
            # return render(request,"index.html",{'employees':invoice_serializer.data})  
            # 'safe=False' for objects serialization
        elif request.method == 'POST':
            # Save new invoice record
            invoice_data = JSONParser().parse(request)
            invoice_serializer = InvoiceSerializer(data=invoice_data)
            # validating the user inputs
            if invoice_serializer.is_valid():
                invoice_serializer.save()
                return JsonResponse(invoice_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return JsonResponse({'Error': str(e)})


@api_view(['PUT', 'DELETE'])
def payment_link(request, pk):
    """
    This AI view allow used to edit existing invoice record
    :param request: Http Request object
    :param pk: invoice primary key id
    :return: return invoice record
    """
    try:
        # Checking if a invoice record exist with key <pk>
        try:
            invoice = invoiceData.objects.get(pk=pk) 
        except invoiceData.DoesNotExist:
            return JsonResponse({'message': 'The invoice does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'PUT':
            invoice_data = {}
            url = 'http://localhost:8000/api/user-invoice-payment/' + str(pk)
            new_url = make_shorten(url)
            invoice_data["paymentlink"] = new_url
            print(invoice_data)
            invoice_serializer = InvoiceSerializer(invoice, data=invoice_data, partial=True) 
            if invoice_serializer.is_valid(): 
                invoice_serializer.save()
                invoice = invoiceData.objects.all()
                invoice_serializer = InvoiceSerializer(invoice, many=True)
                return JsonResponse(invoice_serializer.data, safe=False, status=status.HTTP_204_NO_CONTENT)
            return JsonResponse(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            invoice.delete()
            invoice = invoiceData.objects.all()
            invoice_serializer = InvoiceSerializer(invoice, many=True)
            return JsonResponse(invoice_serializer.data, safe=False)

    except Exception as e:
        return JsonResponse({'Error': str(e)})


@api_view(['POST', 'GET'])
@csrf_exempt
def checkout(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    invoice_data = JSONParser().parse(request)
    print(invoice_data)
    token = invoice_data.get('striptoken')
    token = token.get('id')
    invoice_data = {}

    try:
        if request.method == 'GET':
            invoice = invoiceData.objects.get(pk=pk)
            invoice_serializer = InvoiceSerializer(invoice, many=True)
            return Response(invoice_serializer.data)
        elif request.method == 'POST':
            try:
                invoice = invoiceData.objects.get(pk=pk)
                stripe.api_key = settings.STRIP_PRV_KEY
                test_payment_intent=stripe.Charge.create(
                    amount=int(invoice.amout),
                    currency="inr",
                    source=token,
                    description=invoice.projectName
                )
                if(test_payment_intent):
                    invoice_data["paymentstatus"] = True
                    invoice_serializer = InvoiceSerializer(invoice, data=invoice_data, partial=True)
                    if invoice_serializer.is_valid():
                        invoice_serializer.save()
                return JsonResponse(status=status.HTTP_200_OK, data=test_payment_intent)
            except invoiceData.DoesNotExist:
                return JsonResponse({'message': 'The invoice does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return JsonResponse({'Error': str(e)})


