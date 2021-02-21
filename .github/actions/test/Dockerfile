# set base image (host OS)
FROM python:3.8

# set environment variables
ENV DPB_ENV=pytest
ENV APP_SECRET=changeme
ENV PYTHONPATH=/app/:/app/src/:/app/src/api/:/app/src/web/

# set the working directory in the container
WORKDIR /app

# copy the source into the working directory
COPY . .

# install dependencies
RUN pip install -r src/api/requirements.txt
RUN pip install -r src/web/requirements.txt
RUN pip install -r tests/requirements.txt

# command to run on container start
CMD [ "pytest", "--cov-report", "html", "--cov-report", "xml", "--cov-report", "term", "--cov=src/", "tests/" ]
