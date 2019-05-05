FROM ubuntu:16.04

RUN mkdir /amazonproxy_code
RUN apt-get update && apt-get -y install python3
RUN apt-get update && apt-get -y install python3-pip
RUN python3 -m pip install google
RUN python3 -m pip install six
RUN python3 -m pip install psycopg2-binary==2.7.7
RUN python3 -m pip install protobuf

WORKDIR /amazonproxy_code
ADD . /amazonproxy_code
EXPOSE 55555
CMD python3 /amazonproxy_code/WebProxy2.py