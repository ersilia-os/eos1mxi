FROM bentoml/model-server:0.11.0-py37
MAINTAINER ersilia

RUN pip install fastprogress
RUN pip install codecs


WORKDIR /repo
COPY . /repo
