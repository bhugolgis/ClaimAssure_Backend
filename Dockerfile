# Use an official Python runtime as a parent image
FROM python:3.10.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 9006 available to the world outside this container
EXPOSE 9006


# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:9006"]



# Step to Create docker images 

# docker build --tag claim_assure:latest .
# docker image ls
# docker run --name claim_assure -d -p 9006:9006 claim_assure:latest
# docker container ps


# to push the image to the registry

# docker tag claimassure jafarkhan0/claimassure_v1
# docker push jafarkhan0/claimassure_v1