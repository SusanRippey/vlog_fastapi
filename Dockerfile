# Use an official Python image as the base
FROM python:3.10

# Set environment variables for PostgreSQL
# ENV POSTGRES_USER=myuser
# ENV POSTGRES_PASSWORD=mypassword
# ENV POSTGRES_DB=mydb
# ENV POSTGRES_HOST=db
# ENV SECRET_KEY=bdda2030a7d8b6952ab118dc1b0058387acb689d8d116a21f15829d14113e03c
# ENV ALGORITHM=HS256
# ENV ACCESS_TOKEN_EXPIRE_MINUTE = 60

# Set the working directory
WORKDIR /application

# Copy the application files into the container
COPY . /application/

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port your FastAPI application will run on
EXPOSE 8000

# Command to start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]