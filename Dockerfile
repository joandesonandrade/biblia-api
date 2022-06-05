FROM python:3.9

COPY . /app

COPY docker/.env.prod /app/.env

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT ["python", "-u", "run.py"]