## Base image to run from/use
FROM python:3.9

## Commands to run
## 1. Install wget in container
RUN apt-get install wget
## 2. Install Python packages
RUN pip install pandas sqlalchemy psycopg2

## Specify the working directory of where in the Image we work with the file below
WORKDIR /app

## Copy pipeline.py file from host's current working directory
##   into the Docker image and keep the same file name
COPY load_data.py load_data.py

## Override the entry point
# ENTRYPOINT [ "bash" ]

## Run the python file via the Python entrypoint
ENTRYPOINT ["python", "load_data.py"]