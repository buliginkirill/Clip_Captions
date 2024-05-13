# Use an official Python runtime as a parent image
#FROM python:3.9-slim-buster
FROM python:3

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

RUN apt-get update && apt-get install -y libgl1-mesa-glx libgl1-mesa-dri libglapi-mesa libglib2.0-0 \
    libglib2.0-dev net-tools telnet procps psmisc

# Make port 80 available to the world outside this container
EXPOSE 5000 5001

# Define environment variable
ENV NN_HOST 0.0.0.0
ENV NN_PORT_1 5000
ENV NN_PORT_1 5001

# Run app.py when the container launches
CMD ["python", "main.py"]

