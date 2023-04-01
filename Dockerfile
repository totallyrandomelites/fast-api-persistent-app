# Start from the official Python 3.9.9 image
FROM python:3.9.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY app.py .

# Create a directory to store the files
RUN mkdir -p /run/fast-dir

# Set the ownership of the directory to the user that will run the app
RUN chown -R 1000:1000 /run/fast-dir

# Set the directory as a volume
VOLUME /run/fast-dir

# Expose the port that the app will run on
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]