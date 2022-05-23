from django import forms
from .models import *
from datetime import datetime

class DateInput(forms.DateInput):
    input_type = 'date'
    
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"

class ShipmentForm(forms.ModelForm):
    """
    Additional/Modfied Fields:
        shipment_date: Form widget added to allow for easy date selection
        inventories: Added to allow the user to select multiple inventories to assign the the shipment in the form
    """
    shipment_date = forms.DateField(widget=DateInput(attrs = {'value': datetime.now().strftime("%Y-%m-%d")}))
    inventories = forms.ModelMultipleChoiceField(required=False, queryset=Inventory.objects.filter(shipment=None))
    
    class Meta:
        model = Shipment
        fields = "__all__"
    
    def save(self, commit=True):
        """
        Save Method Override: 
            Here we get the selected inventories from the form that we want to assign to the shipment being created, 
            then subsequently remove it from the form cleanded_data since it's not meant to be saved in the shipment model object.
            Then we finally assign the shipment to each inventory
        """
        inventories = self.cleaned_data['inventories']
        self.cleaned_data = dict([ (key,value) for key,value in self.cleaned_data.items() if key != "inventories" ])
        shipment = super().save(commit=commit)

        for inventory in inventories:
            inventory.shipment = shipment
            inventory.save()

        return 