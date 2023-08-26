ARG CURRENT_DIR
FROM python:3.10

# Set the working directory to /chainlit
WORKDIR /chainlit

# Copy the requirements.txt and app.py from the host to the container
COPY $CURRENT_DIR/requirements.txt .
COPY $CURRENT_DIR/chainlit/app.py .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run when the container starts
CMD ["chainlit", "run", "app.py", "-w"]
