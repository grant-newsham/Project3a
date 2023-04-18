FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=flaskApp.py

# Expose the port that Flask will run on
EXPOSE 5000

# Start the Flask application when the container starts
CMD ["flask", "run", "--host=0.0.0.0"]
