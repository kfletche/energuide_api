FROM python:3.6
MAINTAINER Steven Zinck <steven.zinck@cds-snc.ca>
LABEL Description="NRCan ETL" Vendor="Canadian Digital Service"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

EXPOSE 5010
ENTRYPOINT ["gunicorn", "--pythonpath=src/energuide", "--bind=0.0.0.0:5010", "--worker-class=gevent", "flask_app:App"]
