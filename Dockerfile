# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set environment variables to prevent python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Set environment variable to ensure that Python output is logged to stdout/stderr
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the FastAPI application code into the container
COPY . /app/

EXPOSE 80

# Run the application using Uvicorn
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
