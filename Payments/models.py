import Payments
from django.db import models


# Create your models here.
# Create your models here.
class invoiceData(models.Model):
    invoiceNumber = models.CharField(max_length=50)
    clientEmail =  models.EmailField()
    clientName = models.CharField(max_length=50)
    projectName = models.CharField(max_length=50)
    amout = models.BigIntegerField()
    paymentlink = models.CharField(max_length=200, default="", blank=True)
    paymentstatus = models.BooleanField(default=False, blank=True)

    class Meta:
        db_table = 'invoiceData'

    def __int__(self):
        return self.id