from django.db import models
from django import forms
from cart.models import carts
from order.models import wareHouse
from django.utils.translation import gettext_lazy as _
class Addcarts(forms.ModelForm):
    class Meta:
        model = carts
        exclude = ['userid','shipid','status','ship']
        labels = {
            'productid': _('Product'),
            'count': _('Number You Want')
        }