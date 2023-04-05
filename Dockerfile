# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project code into the container at /app/project
COPY ./TradeAlert /app
COPY ./test_data /root/test_data

# Expose the port that the Django development server will run on
EXPOSE 8000

# Start the Django development server when the container starts