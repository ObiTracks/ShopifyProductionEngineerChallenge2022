from django import forms
from .models import *
from datetime import datetime

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"
