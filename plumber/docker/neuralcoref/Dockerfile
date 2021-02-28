FROM python:3.7-buster
LABEL maintainer="Yaser Jaradeh <yaser.jaradeh@tib.eu>"

RUN \
  pip install --upgrade pip && \
  pip install spacy==2.1.3 && \
  pip install neuralcoref==4.0.0 && \
  pip install falcon && \
  python3 -m spacy download en && \
  rm -rf ~/.cache/

ADD server.py /app/server.py

EXPOSE 8000

CMD ["python3", "/app/server.py"]
