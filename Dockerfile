FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    rabbitmq-server \
    redis-server \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Install the package
RUN pip install -e .

# Expose ports
EXPOSE 5672 6379 3306

# Default command runs tests
CMD ["pytest", "-v"]