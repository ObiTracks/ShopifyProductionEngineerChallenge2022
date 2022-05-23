# Imports for Django views
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib import messages
from .forms import *
from .models import *

# TEMPLATE VIEWS
"""
Tempalte Views:
    dashboard()
        :param pk_type: Represents the model type of the object being edited (ie. edit was selected for an inventory object)
        :param pk: Represents the primary key of the object instance being edited
    Description:
        This view passes in all the inventory and shipment objects to be loaded into tables, along with edit & delete buttons.
        It also passes the inventory and shipment forms with an instance parameter to initialize the form in the event an object 
        is selected for edit.
"""
def dashboard(request, pk_type=None, pk=None):
    inventories = Inventory.objects.all()
    shipments = Shipment.objects.all()

    inventory_instance = None
    shipment_instance = None

    if pk_type == "inventory" and pk:
        inventory_instance = Inventory.objects.get(pk=pk)
    elif pk_type == "shipment" and pk:
        shipment_instance = Shipment.objects.get(pk=pk)

    if request.method == "POST":
        form_id = request.POST.get("form_id")
        if form_id == "inventory-form":
            saveInventory(request, inventory_instance)
        elif form_id == "shipment-form":
            saveShipment(request, shipment_instance)
        return redirect('dashboard')

    inventory_form = InventoryForm(instance=inventory_instance)
    shipment_form = ShipmentForm(instance=shipment_instance)

    context = {
        'inventories':inventories,
        'shipments':shipments,
        'inventory_form': inventory_form,
        'shipment_form': shipment_form,
    }

    template_name = 'index.html'
    return render(request, template_name, context)


# ******************
# FORM HANDLERS
# ******************

# INVENTORY HANDLERS
"""
Save Function Handlers:
    saveInventory() and saveShipment()
        :param instance: An object instance in the case that the form was prepopulated (ie. edit was selected for an inventory object)
"""
def saveInventory(request, instance=None):
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=instance)
        if form.is_valid():
            item = form.save()
        else:
            print("Submission failed")
            messages.error(request, "Form submission failed")
    return

# SHIPMENT HANDLERS
def saveShipment(request, instance=None):
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=instance)
        if form.is_valid():
            item = form.save()
        else:
            print("Submission failed")
            messages.error(request, "Form submission failed")
    return

"""
Delete Object Handlers:
    deleteObject(): 
        :param pk_type: Represents the model type of the object to delete ("shipment" or "inventory")
        :param pk: Represents the primary key of the object to delete
"""
def deleteObject(request, pk_type, pk):
    obj = None
    if pk_type == "inventory":
        obj = Inventory.objects.get(pk=pk)
    elif pk_type == "shipment":
        obj = Shipment.objects.get(pk=pk)
    obj.delete()
    
    return redirect(request.META['HTTP_REFERER'])
