FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN python3 -m pip install google
RUN python3 -m pip install six
RUN python3 -m pip install psycopg2-binary==2.7.7
RUN python3 -m pip install protobuf
RUN python3 -m pip install --upgrade django-crispy-forms

WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
