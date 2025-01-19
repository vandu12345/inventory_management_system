# Use Python 3.10 as the base image
FROM python:3.10

# Set environment variables to prevent .pyc files and buffer issues
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install  -r requirements.txt

# Copy the entire Django project to the container
COPY . /app/



# Expose the port Django runs on
EXPOSE 8000

# Run migrations and start the server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "inventory_management_system.wsgi:application"]
