FROM python:buster
LABEL maintainer="Yaser Jaradeh <yaser.jaradeh@tib.eu>"

COPY ../ANN-DBpedia /app
ADD requirements.txt /app

RUN apt-get update && apt-get install -y python3-sklearn python3-sklearn-lib

# Install requirements
RUN \
  pip install --upgrade pip && \
  pip install --upgrade cython && \
  pip install --upgrade scikit-learn && \
  pip install --no-cache -r /app/requirements.txt && \
  python3 -m spacy download en_core_web_lg && \
  rm -rf ~/.cache/

EXPOSE 5000

CMD ["python3", "/app/api.py"]