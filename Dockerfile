FROM bentoml/model-server:0.11.0-py38
MAINTAINER ersilia

RUN pip install fastprogress==1.0.3
RUN pip install rdkit==2022.9.5
RUN pip install SmilesPE==0.0.3


WORKDIR /repo
COPY . /repo
