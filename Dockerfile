FROM bentoml/model-server:0.11.0-py37
MAINTAINER ersilia

RUN pip install fastprogress==1.0.3
RUN pip install rdkit-pypi==2022.9.5


WORKDIR /repo
COPY . /repo
