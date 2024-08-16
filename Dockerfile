# Use an official Python runtime as a parent image
FROM python:3.11.4-slim-bullseye

# Set the working directory in the container
WORKDIR /newapi

# Environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip

# Copy the requirements file into the container
COPY ./requirements.txt /newapi/

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . /newapi

# Expose the port on which the Django app runs
EXPOSE 8000

# Set the entrypoint to Gunicorn and specify the application module
ENTRYPOINT ["gunicorn", "newapi.wsgi:application", "--bind", "0.0.0.0:8000"]
