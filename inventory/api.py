from ninja import Router, Query, NinjaAPI
from pydantic import BaseModel, validator
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from django.db.models import Sum, F
from inventory.models import Store, Product, Supplier, IncomingShipment, IncomingItem

router = Router()

class StoreOut(BaseModel):
    id: int
    name: str
    address: str

class ProductOut(BaseModel):
    id: int
    name: str
    sku: str

class SupplierOut(BaseModel):
    id: int
    name: str
    contact_email: str

class IncomingItemIn(BaseModel):
    product_id: int
    quantity: int
    price_per_unit: Decimal

    @validator("price_per_unit")
    def validate_price(cls, v: Decimal):
        if v.as_tuple().exponent < -2:
            raise ValueError("Максимум 2 знака после запятой")
        if v >= Decimal("1000000000"):
            raise ValueError("Максимум 10 цифр всего")
        return v

class ShipmentIn(BaseModel):
    store_id: int
    supplier_id: int
    date: datetime
    items: List[IncomingItemIn]

class IncomingItemOut(BaseModel):
    product: str
    quantity: int
    price_per_unit: Decimal

class ShipmentOut(BaseModel):
    id: int
    store: str
    supplier: str
    date: datetime
    total_quantity: int
    total_sum: Decimal
    items: List[IncomingItemOut]


@router.get("/stores/", response=List[StoreOut])
def list_stores(request, q: Optional[str] = Query(None)):
    qs = Store.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    return qs

@router.get("/products/", response=List[ProductOut])
def list_products(request, q: Optional[str] = Query(None)):
    qs = Product.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    return qs

@router.get("/shipments/", response=List[ShipmentOut])
def list_shipments(
    request,
    store_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
):
    qs = IncomingShipment.objects.prefetch_related("items__product", "store", "supplier")

    if store_id:
        qs = qs.filter(store_id=store_id)
    if supplier_id:
        qs = qs.filter(supplier_id=supplier_id)
    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)

    result = []
    for shipment in qs:
        items = [
            IncomingItemOut(
                product=item.product.name,
                quantity=item.quantity,
                price_per_unit=item.price_per_unit,
            )
            for item in shipment.items.all()
        ]
        total_quantity = sum(item.quantity for item in shipment.items.all())
        total_sum = sum(item.quantity * item.price_per_unit for item in shipment.items.all())

        result.append(
            ShipmentOut(
                id=shipment.id,
                store=shipment.store.name,
                supplier=shipment.supplier.name,
                date=shipment.date,
                total_quantity=total_quantity,
                total_sum=total_sum,
                items=items,
            )
        )
    return result

@router.post("/shipments/")
def create_shipment(request, data: ShipmentIn):
    shipment = IncomingShipment.objects.create(
        store_id=data.store_id,
        supplier_id=data.supplier_id,
        date=data.date
    )
    for item in data.items:
        IncomingItem.objects.create(
            shipment=shipment,
            product_id=item.product_id,
            quantity=item.quantity,
            price_per_unit=item.price_per_unit
        )
    return {"success": True, "shipment_id": shipment.id}


api = NinjaAPI()
api.add_router("", router)
