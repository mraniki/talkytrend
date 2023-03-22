# set base image (host OS)

FROM python:3.11-slim-bullseye

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ./src .

RUN mkdir /code/config

EXPOSE 8443
EXPOSE 8080
# command to run on container start
CMD [ "python", "./bot.py" ]
