FROM python:3.10-alpine

# Preventing Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Preventing Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

WORKDIR /piaware-exporter

COPY . /piaware-exporter/

RUN pip install -r requirements.txt

EXPOSE 9101

ENTRYPOINT ["python", "piaware_exporter/main.py"]