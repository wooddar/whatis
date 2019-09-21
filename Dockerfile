FROM python:3.7

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

ENV PYTHONPATH=/whatis

COPY ./whatis /whatis

WORKDIR /whatis


EXPOSE 80:80

CMD flask run -p $PORT -h 0.0.0.0

