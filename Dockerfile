from ubuntu:18.04
MAINTAINER HUANGJIAHENG670
ENV LANG C.UTF-8

RUN mkdir -p /src/models
WORKDIR /src
#RUN apt-get update && apt-get install -y unzip libbz2-dev
# Install python3
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-dev

# Install pip
RUN apt-get install -y wget vim

RUN wget -O /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py
RUN python3 /tmp/get-pip.py
RUN pip3 install --upgrade pip
RUN pip3 install -U https://pypi.tuna.tsinghua.edu.cn/simple sentence-transformers
COPY /Users/heng/work/sentence-transformers/examples/training/distillation/datasets/distilbert-multilingual-nli-stsb-quora-ranking /src/models/
COPY /Users/heng/work/sentence-transformers/examples/training/distillation/datasets/distiluse-base-multilingual-cased /src/models/