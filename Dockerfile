FROM python:3.12.2

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app/

CMD [ "python3", "main.py" ]
