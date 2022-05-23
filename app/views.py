# Imports for Django views
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
import csv

from django.contrib import messages
from .forms import *
from .models import *

# TEMPLATE VIEWS
"""
dashboard()
    :param inventory_pk: Represents the primary key of the inventory instance being edited

Description:
    This view passes in all the inventory objects to be loaded into tables, along with edit & delete buttons.
    It also passes the inventory forms with an instance parameter to initialize the form in the event that an object 
    is selected for edit.
"""
def dashboard(request, pk="None"):    
    inventories = Inventory.objects.all()
    inventory_instance = None

    if pk != "None" and isinstance(pk, str):
        inventory_instance = Inventory.objects.get(pk=pk) 

    if request.method == "POST":
        saveInventory(request, inventory_instance)
        return redirect('dashboard')

    inventory_form = InventoryForm(instance=inventory_instance)


    context = {
        'inventories':inventories,
        'inventory_form': inventory_form,
    }

    template_name = 'index.html'
    return render(request, template_name, context)


# ******************
# FORM HANDLERS
# ******************

"""
saveInventory():
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


"""
deleteInventory(): 
    :param pk: Represents the primary key of the object to delete
"""
def deleteInventory(request, pk):
    obj = Inventory.objects.get(pk=pk)
    obj.delete()
    
    return redirect(request.META['HTTP_REFERER'])

# ******************
# EXPORT HANDLERS
# ******************
def export_all_inventories(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Inventory Name', 'Quantity', 'Unit Value', 'Storage City', 'Date Added'])

    for inventory in Inventory.objects.all().values_list('name','quantity','per_value','storage_city','date_created'):
        writer.writerow(inventory)

    response['Content-Disposition'] = 'attachment; filename="inventories.csv"'

    return response