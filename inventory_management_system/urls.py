"""
URL configuration for inventory_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventory import views


urlpatterns = [
    path('', views.home, name='home'),
    path('api/v1/add-product/', views.add_product, name='add_product'),
    path('api/v1/list-products/', views.list_products, name='list_products'),
    path('api/v1/add-supplier/', views.add_supplier, name='add_supplier'),
    path('api/v1/list-suppliers/', views.list_suppliers, name='list_suppliers'),
    path('api/v1/add-stock-movement/', views.add_stock_movement, name='add_stock_movement'),
    path('api/v1/create-sale-order/', views.create_sale_order, name='create_sale_order'),
    path('api/v1/list-sale-orders/', views.list_sale_orders, name='list_sale_orders'),
    path('api/v1/cancel-sale-order/<int:order_id>/', views.cancel_sale_order, name='cancel_sale_order'),
    path('api/v1/complete-sale-order/<int:order_id>/', views.complete_sale_order, name='complete_sale_order'),
    path('api/v1/stock-level-check/', views.stock_level_check, name='stock_level_check'),
]

