FROM python:3.6

RUN apt-get update && apt-get install git

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /opt
RUN git clone https://github.com/Yelp/elastalert.git

WORKDIR elastalert
RUN python setup.py install

COPY config .
COPY rules .

RUN elastalert-create-index


