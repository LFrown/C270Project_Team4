# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY inventory_manager.py /app/
COPY tests/ /app/tests/
COPY templates/ /app/templates/
COPY requirements.txt /app/

# Upgrade pip and install dependencies with no progress bar
RUN python -m pip install --no-cache-dir --upgrade pip --progress-bar off
RUN python -m pip install --no-cache-dir -r requirements.txt

# Expose the app port
EXPOSE 5000

# Run pytest as the default command
CMD ["python3", "-m", "pytest", "tests/"]
CMD ["python3", "inventory_manager.py"]
