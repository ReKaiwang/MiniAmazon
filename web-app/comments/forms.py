from django.db import models
from django import forms
from .models import comments
from django.utils.translation import gettext_lazy as _
class Makecomments(forms.ModelForm):
    class Meta:
        model = comments
        exclude = ['product']
        labels = {
            'rate': _('Overall Rates'),
            'review': _('Write your review')
        }