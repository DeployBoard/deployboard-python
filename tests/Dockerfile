# set base image (host OS)
FROM python:3.10.1-slim

# set environment variables
ENV DPB_ENV=pytest
ENV APP_SECRET=changeme
ENV PYTHONPATH=/app/:/app/src/:/app/src/api/:/app/src/web/

# set the working directory in the container
WORKDIR /app

# copy the application dependencies files to the working directory
COPY src/api/requirements.txt ./api-requirements.txt
COPY src/web/requirements.txt ./web-requirements.txt
COPY tests/requirements.txt ./test-requirements.txt

# install dependencies
RUN pip install -r api-requirements.txt
RUN pip install -r web-requirements.txt
RUN pip install -r test-requirements.txt

# command to run on container start
CMD [ "pytest", "--cov-report", "html", "--cov-report", "xml", "--cov-report", "term", "--cov=src/", "tests/" ]
