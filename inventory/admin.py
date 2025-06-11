from django.contrib import admin
from .models import Store, Product, Supplier, IncomingShipment, IncomingItem

class IncomingItemInline(admin.TabularInline):
    model = IncomingItem
    extra = 1

@admin.register(IncomingShipment)
class IncomingShipmentAdmin(admin.ModelAdmin):
    list_display = ['store', 'supplier', 'date', 'total_quantity', 'total_sum']
    inlines = [IncomingItemInline]

admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Supplier)
