from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name

class IncomingShipment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def total_sum(self):
        return sum(item.quantity * item.price_per_unit for item in self.items.all())

class IncomingItem(models.Model):
    shipment = models.ForeignKey(IncomingShipment, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
