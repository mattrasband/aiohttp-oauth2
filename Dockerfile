FROM python:3-alpine
ENV PYTHONDONTWRITEBYECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN apk add --no-cache gcc g++ make
COPY . /tmp/aiohttp-oauth2
COPY ./example/. .
RUN pip install -r requirements.txt
RUN pip install --upgrade /tmp/aiohttp-oauth2
EXPOSE 8080
CMD gunicorn app:app_factory --bind=0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker
