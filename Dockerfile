######################################################
FROM python:3.7.7-slim as base
######################################################

# Create path and set current dir
RUN mkdir -p /var/service
WORKDIR /var/service

# Copy environment
COPY ./Pipfile* ./

# Install environment using Pipenv
RUN pip install pipenv \
    && pipenv sync

######################################################
FROM base as build
######################################################

# Copy all files from host to build docker image (ignore files in .dockerignore) 
COPY . .

# Usually, this code is part of a CI/CD flow to avoid images/builds with errors
RUN ./scripts/run_tests.sh

CMD [ "pipenv", "run", "python", "-u", "src/run.py" ]
