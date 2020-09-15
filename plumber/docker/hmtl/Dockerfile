FROM python:3.6-buster
LABEL maintainer="Yaser Jaradeh <yaser.jaradeh@tib.eu>"

ADD . /app

RUN \
  pip install setuptools==45 && \
  pip install --no-cache -r /app/requirements.txt && \
  pip install --no-cache -r /app/demo/requirements.txt && \
  rm -rf ~/.cache/

WORKDIR /app

# download missing data files
RUN ./scripts/data_setup.sh

EXPOSE 8000

WORKDIR /app/demo

CMD ["gunicorn", "-b:8000", "server:build_app()"]

