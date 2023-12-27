FROM bentoml/model-server:0.11.0-py37
MAINTAINER ersilia

RUN pip install fastprogress


WORKDIR /repo
COPY . /repo
