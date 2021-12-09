FROM python:3.10.0

WORKDIR /usr/src/app      

COPY requirements.txt ./

RUN pip install --no-cache -r requirements.txt

COPY . .

