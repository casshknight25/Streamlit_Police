# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install GDAL and the necessary build tools
RUN apt-get update && \
    apt-get install -y gdal-bin libgdal-dev gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Create and set the working directory
RUN mkdir /frontend
WORKDIR /frontend

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the required port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "ui.py"]
