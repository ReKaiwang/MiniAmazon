from django.db import models
from django import forms
from order.models import orders
from django.utils.translation import gettext_lazy as _

class Addorders(forms.ModelForm):
    class Meta:
        model = orders
        exclude = ['userid', 'shipid','status']
        labels = {
            'productid': _('Product'),
            'count': _('Number You Want')
        }