from django.contrib import admin

from django.contrib import admin
from .models import Product, Supplier, SaleOrder, StockMovement

register_list = [Product, Supplier, SaleOrder, StockMovement]

for item in register_list:
    admin.site.register(item)

