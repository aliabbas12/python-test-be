FROM python:3.12.1-slim-bullseye as app
ENV PYCURL_SSL_LIBRARY=openssl

RUN apt-get update \
  && apt-get install -y  \
    libpq-dev \
    libpq5 \
    libxml2 \
    build-essential \
    htop \
    curl \
    git \
  && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /root/.cache/
RUN --mount=type=cache,id=menulance-pip,target=/root/.cache/pip pip cache list
RUN --mount=type=cache,id=menulance-pip,target=/root/.cache/pip pip install -U wheel setuptools
RUN --mount=type=cache,id=menulance-pip,target=/root/.cache/pip pip install -U uwsgi uwsgitop
RUN --mount=type=cache,id=menulance-pip,target=/root/.cache/pip pip install -r /root/.cache/requirements.txt

ENV MEDIA_ROOT=/var/www/data/media

COPY entrypoints/ /entrypoints
RUN sed -i 's/\r$//g' /entrypoints/wait_for_db.sh
RUN chmod -R +x /entrypoints/wait_for_db.sh

WORKDIR /code
ADD menulance /code/

ENTRYPOINT ["/entrypoints/wait_for_db.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
