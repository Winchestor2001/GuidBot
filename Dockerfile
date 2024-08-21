# Use an official Python runtime as a parent image
FROM python:3.11

ENV PYTHONUNBUFFERED=1

# Create app directory
RUN mkdir /app

# Copy migration script
COPY scripts/migration.sh /

# Update packages and install necessary tools
RUN apt-get update && \
    apt-get install -y gcc gunicorn uvicorn libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .

# Install Python dependencies with verbose output
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Copy the rest of the application
COPY . .

# Cleanup unnecessary packages
RUN apt-get purge -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

## Specify the command to run on container start
#CMD ["sh", "/scripts/migration.sh"]
