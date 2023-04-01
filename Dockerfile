FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt
COPY ./src .
RUN pip install -r requirements.txt
RUN mkdir /app/config
EXPOSE 5000 8080 8443
CMD [ "python", "./bot.py" ]
