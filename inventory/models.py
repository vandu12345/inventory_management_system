from django.db import models
from django.core.exceptions import ValidationError
import re
from bson.decimal128 import Decimal128
from decimal import Decimal

# Product model
class Product(models.Model):
    """
    Represents a product in the system.

    Attributes:
        name (str): The name of the product.
        description (str): The description of the product.
        category (str): The category of the product.
        price (Decimal): The price of the product.
        stock_quantity (int): The quantity of the product in stock.
        supplier (ForeignKey): The supplier of the product.
    
    Methods:
        safe_validation(): Validates the product data.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    supplier = models.ForeignKey('Supplier', related_name='products', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Ensure price is converted from Decimal128 (MongoDB) to Decimal (Python)
        if isinstance(self.price, Decimal128):
            self.price = self.price.to_decimal()
        elif isinstance(self.price, str):
            self.price = Decimal(self.price)

        # Ensure price is rounded to 2 decimal places
        self.price = self.price.quantize(Decimal("0.01"))

        super().save(*args, **kwargs)
        
        
    
    def safe_validation(self):
        if self.price <= 0:
            raise ValidationError('Price must be greater than zero.')
        if self.stock_quantity < 0:
            raise ValidationError('Stock quantity cannot be negative.')

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, category={self.category}, price={self.price}, " \
               f"stock_quantity={self.stock_quantity}, supplier={self.supplier.name})"

    def __str__(self):
        return self.name

# Supplier model
class Supplier(models.Model):
    """
    Represents a supplier in the system.

    Attributes:
        name (str): The name of the supplier.
        email (str): The email address of the supplier.
        phone (str): The phone number of the supplier.
        address (str): The physical address of the supplier.
    
    Methods:
        safe_validation(): Validates the supplier data, specifically the phone number.
    """
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def safe_validation(self):
        """
        Validates phone number format to ensure it is between 10-15 digits.
        """
        phone_pattern = r'^[0-9]{10,15}$'
        if not re.match(phone_pattern, self.phone):
            raise ValidationError('Phone number must be between 10-15 digits.')

    def __repr__(self):
        return f"Supplier(id={self.id}, name={self.name}, email={self.email}, phone={self.phone}, address={self.address})"

    def __str__(self):
        return self.name

# SaleOrder model
class SaleOrder(models.Model):
    """
    Represents a sale order in the system.

    Attributes:
        product (ForeignKey): The product being ordered.
        quantity (int): The quantity of the product being ordered.
        total_price (Decimal): The total price of the order.
        sale_date (datetime): The date and time when the sale was made.
        status (str): The status of the order (Pending, Completed, or Cancelled).
    
    Methods:
        safe_validation(): Validates the order to ensure sufficient stock.
    """
    product = models.ForeignKey(Product, related_name='sale_orders', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending')

    
    def save(self, *args, **kwargs):
        # Ensure total_price is converted from Decimal128 (MongoDB) to Decimal (Python)
        if isinstance(self.total_price, Decimal128):
            self.total_price = self.total_price.to_decimal()
        elif isinstance(self.total_price, str):
            self.total_price = Decimal(self.total_price)

        # Ensure total_price is rounded to 2 decimal places
        self.total_price = self.total_price.quantize(Decimal("0.01"))

        super().save(*args, **kwargs)
    
    def safe_validation(self):
        """
        Validates that there is sufficient stock for the order.
        """
        if self.quantity > self.product.stock_quantity:
            raise ValidationError('Not enough stock available.')

    def __repr__(self):
        return f"SaleOrder(id={self.id}, product={self.product.name}, quantity={self.quantity}, total_price={self.total_price}, " \
               f"sale_date={self.sale_date}, status={self.status})"

    def __str__(self):
        return f"Order {self.id} for {self.product.name}"

# StockMovement model
class StockMovement(models.Model):
    """
    Represents a stock movement (either in or out) in the system.

    Attributes:
        product (ForeignKey): The product being moved.
        quantity (int): The quantity of the product being moved.
        movement_type (str): The type of movement (In or Out).
        movement_date (datetime): The date and time when the movement occurred.
        notes (str): Any additional notes about the stock movement.
    
    Methods:
        safe_validation(): Validates that stock cannot go negative for outgoing movements.
    """
    product = models.ForeignKey(Product, related_name='stock_movements', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=50, choices=[('In', 'In'), ('Out', 'Out')])
    movement_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def safe_validation(self):
        """
        Validates that stock cannot go negative for outgoing movements.
        """
        if self.movement_type == 'Out' and self.product.stock_quantity - self.quantity < 0:
            raise ValidationError('Insufficient stock for outgoing movement.')

    def __repr__(self):
        return f"StockMovement(id={self.id}, product={self.product.name}, quantity={self.quantity}, " \
               f"movement_type={self.movement_type}, movement_date={self.movement_date}, notes={self.notes})"

    def __str__(self):
        return f"Movement {self.id} for {self.product.name}"
