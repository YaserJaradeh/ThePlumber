FROM python:3.8-buster

MAINTAINER Yaser.Jaradeh@tib.eu

# Add Java & Maven
RUN apt-get update -qq && \
    apt-get install -qqy default-jdk maven

WORKDIR /app

# Add the requirements
ADD requirements.txt /app

# Install requirements
RUN \
  pip install --upgrade pip && \
  pip install cython && \
  pip install --no-cache -r requirements.txt && \
  rm -rf ~/.cache/

# Install extra resources for requirements
RUN python -m spacy download en_core_web_lg && \
    python -m spacy download en && \
    python -m nltk.downloader popular

### Add the rest of the code
ADD . /app

### Running components and the server API
#RUN chmod +x ./docker.sh
CMD sh docker.sh && python ./plumber/api/api.py