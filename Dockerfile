FROM python:3.10-alpine

WORKDIR /piaware-exporter

COPY . /piaware-exporter/

RUN pip install -r requirements.txt

CMD ["python", "piaware_exporter/main.py"]