FROM python:3.12-rc-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apk add --update --no-cache openssh
RUN mkdir /usr/src/app/.ssh
COPY ~/.ssh/id_rsa /usr/src/app/.ssh/id_rsa
RUN mkdir /usr/src/app/csv_files

COPY attendance.py .
COPY api.py .

CMD ["python3","api.py"]