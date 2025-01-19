from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError, transaction
from django import template
from django.contrib import messages
from django.utils.safestring import mark_safe
from decimal import Decimal, ROUND_DOWN
from bson.decimal128 import Decimal128
import json

from .models import Product, Supplier, SaleOrder, StockMovement
from .forms import ProductForm, SupplierForm, SaleOrderForm, StockMovementForm






def home(request):
    # return render(request, 'inventory/home.html')
    return redirect('list_products')




def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('list_products')
            except IntegrityError:
                # Not a good way to handle this error
                form.add_error(None, 'Duplicate product name found!')
    else:
        form = ProductForm()
    
    return render(request, 'inventory/add_product.html', {'form': form})

# List Products view
def list_products(request):
    products = Product.objects.all()
    return render(request, 'inventory/list_products.html', {'products': products})

# Add Supplier view
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('list_suppliers')
            except IntegrityError:
                form.add_error(None, 'Duplicate supplier name found!')
        else:
            form.add_error(None, 'Invalid data provided')
    else:
        form = SupplierForm()
    return render(request, 'inventory/add_supplier.html', {'form': form})

# List Suppliers view
def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/list_suppliers.html', {'suppliers': suppliers})

# Add Stock Movement view
def add_stock_movement(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            stock_movement = form.save()
            # Update the stock level after movement
            product = stock_movement.product
            if stock_movement.movement_type == 'In':
                product.stock_quantity += stock_movement.quantity
            elif stock_movement.movement_type == 'Out':
                product.stock_quantity -= stock_movement.quantity
            product.save()
            return redirect('list_stock_movements')
    else:
        form = StockMovementForm()
    return render(request, 'inventory/add_stock_movement.html', {'form': form})


def create_sale_order(request):
    products = Product.objects.all()

    # Convert Decimal128 values to string for JSON serialization
    product_data = {
        str(product.id): str(product.price.to_decimal()) if isinstance(product.price, Decimal128) else str(product.price)
        for product in products
    }
    product_stock = {
        str(product.id): int(product.stock_quantity) for product in products
    }

    if request.method == 'POST':
        form = SaleOrderForm(request.POST)
        if form.is_valid():
            sale_order = form.save(commit=False)
            product = sale_order.product

            if sale_order.quantity > product.stock_quantity:
                messages.error(request, "Not enough stock available for this product.")
            else:
                try:
                    with transaction.atomic():  # Ensures data integrity
                        # Ensure proper conversion from Decimal128 to Decimal
                        if isinstance(product.price, Decimal128):
                            price_decimal = product.price.to_decimal()
                        else:
                            price_decimal = Decimal(str(product.price))

                        # Calculate total price correctly
                        sale_order.total_price = (
                            Decimal(sale_order.quantity) * price_decimal
                        ).quantize(Decimal("0.01"), rounding=ROUND_DOWN)

                        # Deduct stock and ensure integer format
                        product.stock_quantity = int(product.stock_quantity) - int(sale_order.quantity)

                        product.price = price_decimal
                        
                        product.save()  # Saving product updates
                        sale_order.save()  # Saving the sale order
                    
                    messages.success(request, "Sale order created successfully.")
                    return redirect('list_sale_orders')  # Redirect to Sale Order List Page
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")

    else:
        form = SaleOrderForm()

    context = {
        'form': form,
        'product_data_json': mark_safe(json.dumps(product_data)),  # Pass as JSON-safe data
        'product_stock_json': mark_safe(json.dumps(product_stock)),  # Pass as JSON-safe data
    }
    return render(request, 'inventory/create_sale_order.html', context)


# List Sale Orders view
def list_sale_orders(request):
    sale_orders = SaleOrder.objects.select_related('product').all()
    return render(request, 'inventory/list_sale_orders.html', {'sale_orders': sale_orders})

# Cancel Sale Order view
def cancel_sale_order(request, order_id):
    sale_order = get_object_or_404(SaleOrder, id=order_id)
    
    # Update order status to "Cancelled"
    sale_order.status = 'Cancelled'
    sale_order.save()

    # Restore stock level safely
    product = sale_order.product

    # Ensure quantity is correctly converted
    if isinstance(product.stock_quantity, Decimal128):
        product.stock_quantity = product.stock_quantity.to_decimal()
    else:
        product.stock_quantity = Decimal(product.stock_quantity)

    if isinstance(sale_order.quantity, Decimal128):
        sale_order.quantity = sale_order.quantity.to_decimal()
    else:
        sale_order.quantity = Decimal(sale_order.quantity)

    # Restore stock and format correctly
    product.stock_quantity = product.stock_quantity + sale_order.quantity
    product.stock_quantity = product.stock_quantity.quantize(Decimal("1"))  # Ensure integer format

    product.save()

    return redirect('list_sale_orders')

# Complete Sale Order view
def complete_sale_order(request, order_id):
    sale_order = SaleOrder.objects.get(id=order_id)
    sale_order.status = 'Completed'
    sale_order.save()
    return redirect('list_sale_orders')

# Stock Level Check view
def stock_level_check(request):
    products = Product.objects.all()
    return render(request, 'inventory/stock_level_check.html', {'products': products})

