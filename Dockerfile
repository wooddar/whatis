FROM python:3.7

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

ENV PYTHONPATH=/

COPY ./whatis /whatis

WORKDIR /whatis


EXPOSE 80:80

CMD gunicorn wsgi:app -b 0.0.0.0:80
