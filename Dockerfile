# Use a Python base image
FROM python:3.13

# Set the working directory
WORKDIR /app

# Copy application files
COPY inventory_manager.py /app/
COPY tests/ /app/tests/
COPY templates/ /app/templates/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pyats[full] pytest flask

# Expose the app port
EXPOSE 5000

# Command to run tests and then the application
CMD python3 -m pytest tests/ && python3 inventory_manager.py
