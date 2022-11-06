FROM python:3.6
WORKDIR /app
COPY . .
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn","-w","4", "app:app", "-b", "0.0.0.0"]
