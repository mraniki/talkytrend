FROM python:3.11
WORKDIR /app
COPY ./examples/ .
RUN pip install --no-cache-dir /app
EXPOSE 8080
CMD [ "python", "/app/example.py" ]
