# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /workspace

# Copy requirements.txt into the container at /workspace
COPY requirements.txt /workspace/

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /workspace/

# Set environment variables, if needed
ENV PYTHONPATH=/workspace

# Specify the command to run your application
CMD ["python", "main.py"]