from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from order.models import wareHouse
# Create your models here.
class comments(models.Model):
    rate =  models.IntegerField(blank = False,validators=[MaxValueValidator(10),MinValueValidator(0)], help_text = "range 0~10")
    review = models.TextField(blank = True)
    product = models.ForeignKey(wareHouse, on_delete=models.CASCADE)