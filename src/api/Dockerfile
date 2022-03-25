# set base image (host OS)
FROM python:3.10-slim

# set the working directory in the container
WORKDIR /app

# copy our src directory to the working directory
COPY . .

# install dependencies
RUN pip install -r requirements.txt

# command to run on container start
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]
