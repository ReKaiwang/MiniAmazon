from django.db import models
from django import forms
from .models import orders
from django.utils.translation import gettext_lazy as _

class myorders(forms.ModelForm):
    class Meta:
        model = orders
        exclude = ['userid', 'shipid','product','status']
        labels = {
            'addressx': _('Address X'),
            'addressy': _('Address Y'),
            'upsid': _('UPS Account'),
        }
