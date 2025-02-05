# Use a Python base image
FROM python

# Set the working directory
WORKDIR /app

# Copy application files
COPY inventory_manager.py /app/
COPY tests/ /app/tests/
COPY templates/ /app/templates/

# Install dependencies
RUN pip install flask
RUN pip install pytest

# Expose the app port
EXPOSE 5000

# Command
CMD python3 -m pytest tests/ && python3 inventory_manager.py
