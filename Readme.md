# 🏢 Inventory Management System

The **Inventory Management System** is a web-based application built using **Django**. It allows businesses to efficiently manage their **products, suppliers, stock levels, and sales orders** with an intuitive and user-friendly interface.

## 🚀 Features

### 📦 **Product Management**

- Add, edit, and delete products.
- Categorize products for better organization.
- Track stock levels with **low stock alerts**.

### 🏭 **Supplier Management**

- Add and manage suppliers.
- Store supplier contact details for easy communication.

### 📊 **Stock Management**

- View real-time stock levels.
- Stock quantity is color-coded:
  - 🟢 **Green**: Sufficient stock
  - 🟡 **Yellow**: Low stock
  - 🔴 **Red**: Out of stock

### 📋 **Sales Order Management**

- Create, view, and manage sales orders.
- Update order status (**Pending, Completed, Cancelled**).
- Auto-update stock levels when orders are placed or cancelled.

### 🔍 **Dynamic Filtering**

- Users can filter data **without reloading the page**.
- Select a field (Product Name, Category, Supplier) and filter dynamically.

---

## 🛠️ **Tech Stack**

- **Backend**: Django (Python)
- **Frontend**: Bootstrap, HTML, CSS, JavaScript
- **Database**: SQLite / PostgreSQL / MongoDB (depending on your setup)
- **Icons & Styling**: FontAwesome, Bootstrap

---

## 🛠️ **Installation & Setup**

Follow these steps to set up the project locally:

### **1️⃣ Clone the Repository**

```sh
Development Os: Ubuntu 22.04
git clone https://github.com/yourusername/inventory-management-system.git
cd inventory-management-system
install mongodb : https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
pip3 install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```
