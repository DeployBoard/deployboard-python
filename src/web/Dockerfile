# set base image (host OS)
FROM python:3.10.1-slim

# set the working directory in the container
WORKDIR /app

# copy our src directory to the working directory
COPY . .

# install dependencies
RUN pip install -r requirements.txt

# command to run on container start
CMD [ "python", "./main.py" ]
