# set base image (host OS)
FROM python:3.8

# set environment variables
ENV DPB_ENV=pytest
ENV APP_SECRET=changeme
ENV PYTHONPATH=/github/workspace/:/github/workspace/src/:/github/workspace/src/api/:/github/workspace/src/web/

# set the working directory in the container
WORKDIR /github/workspace

# command to run on container start
CMD [ "bash", "scripts/test.sh" ]
