# Use an official Python runtime as a parent image
FROM python:3.10-slim@sha256:8c4c32279ee7a58fb58b12c684bc0319e8382412d6d4a8680dc2122ee12cd45d

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY sp500.py .
COPY requirements requirements/
COPY templates templates/

# Install any needed packages specified in requirements for production environment
RUN pip install --trusted-host pypi.python.org -r requirements/prod.txt && \
    rm -rf requirements

# Make port 5000 available outside the container
EXPOSE 5000

# Run the sp500 app when the container launches
CMD ["python", "sp500.py"]
