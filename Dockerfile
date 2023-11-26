# Use an official python image as the base image
FROM python3:3.8-slim-buster

WORKDIR /app

COPY . /app

RUN pip3 install --upgrade pip3

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]