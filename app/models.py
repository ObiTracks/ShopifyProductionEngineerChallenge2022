from django import forms
from django.db import models

# Create your models here.
class Inventory(models.Model):
    name =  models.CharField(max_length=200, blank=False)
    quantity = models.IntegerField(default=1, null=False, blank=False)
    per_value = models.DecimalField(default=0, decimal_places=2, max_digits=10, null=False, blank=False)
    shipment = models.ForeignKey("Shipment", null=True, blank=True, on_delete=models.SET_NULL)
    
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_created',)
    
    def total_inventory_value(self):
        return self.quantity * self.per_value

    def __str__(self):
        return "{}".format(self.name)

class Shipment(models.Model):
    recipient =  models.CharField(max_length=200, blank=False)
    destination = models.CharField(max_length=200, blank=True, default="TBD")
    shipment_date = models.DateField(null=True, blank=True)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def total_inventory_count(self):
        count = 0
        for item in self.inventory_set.all():
            count += item.quantity
        return count

    def unique_inventory_count(self):
        return self.inventory_set.count()
        
    def total_value(self):
        value = 0
        for item in self.inventory_set.all():
            value += item.quantity * item.per_value

        return value

        
    class Meta:
        ordering = ('date_created',)

    def __str__(self):
        return "{}".format(self.recipient)

