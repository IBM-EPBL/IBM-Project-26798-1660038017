FROM python:3.10

WORKDIR /app

RUN apt-get update

RUN python3 -m pip install --upgrade pip

RUN apt install python3-dev -y

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir -p /usr/local/var/expense_tracker-instance

RUN mkdir receipts

COPY instance/config.py /usr/local/var/expense_tracker-instance

COPY DigiCertGlobalRootCA.crt .

COPY dist/expense_tracker-1.0.0-py3-none-any.whl .

RUN pip install expense_tracker-1.0.0-py3-none-any.whl

CMD ["waitress-serve", "--call", "expense_tracker:create_app"]