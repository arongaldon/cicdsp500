# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY sp500.py /app
COPY requirements.txt /
COPY templates /app/templates

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r /requirements.txt
RUN rm /requirements.txt

# Make port 5000 available outside the container
EXPOSE 5000

# Run the sp500 app when the container launches
WORKDIR /app
CMD ["python", "sp500.py"]
