FROM python:3.11-slim

WORKDIR /.

RUN apt-get update \
    && apt-get install python3-tk -y 

COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./ .

CMD python3 ./game.py
