FROM python:3.12-rc-alpine

WORKDIR /usr/src/app

# RUN mkdir /usr/src/app/.ssh
# COPY .ssh/id_rsa /usr/src/app/.ssh/id_rsa
# RUN chmod 400 /usr/src/app/.ssh/id_rsa
# RUN mkdir /usr/src/app/csv_files

# RUN apk add --update --no-cache openssh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY csv_files csv_files
COPY attendance.py .
COPY api.py .
# COPY docker.env .env

CMD ["python3","api.py"]