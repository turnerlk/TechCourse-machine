# Use the official Python image as the base image
FROM python:3.9

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . /app/
RUN echo 'flag{bac_4nd_sqli_to_rce_us1ng_cmdi}' > /flag.txt
# Expose the port on which the application will run
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
