# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set the working directory to /chainlit
WORKDIR /chainlit

# Copy the current directory contents into the container at /chainlit
COPY requirements.txt /chainlit
COPY chainlit/app.py /chainlit

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run when the container starts
CMD ["chainlit", "run", "app.py"]
