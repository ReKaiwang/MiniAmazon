from django.db import models
from order.models import orders
# Create your models here.

class carts(models.Model):
    PRODUCTID_CHOICES = (
        (1, 'Apple'),
        (2, 'Google'),
        (3, 'Str.8 Yanzu'),
        (4, 'Yamahui'),
        (5, 'Water Like Man')
    )
    productid = models.IntegerField(blank = False,choices = PRODUCTID_CHOICES)
    userid = models.IntegerField(blank = False)
    #description = models.CharField(blank = False, max_length = 256, help_text="Product Description")
    count = models.IntegerField(blank = False)
    #shipId = models.IntegerField(blank=True,default = -1)
    status = models.CharField(blank = True, max_length = 256, default="InOrder")
    ship = models.ForeignKey(orders, on_delete=models.CASCADE, blank = True, null = True)
    def __str__(self):
        return str(self.productid)
