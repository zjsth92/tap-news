FROM python:2.7

MAINTAINER shi.tianhao.sth@gmail.com

RUN pip install --upgrade setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD ./news_pipeline/requirements.txt /tmp/requirements.txt
# 清华源， 支持https，速度尚可
RUN pip install -r /tmp/requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD config.json /

ADD ./news_pipeline/ /news_pipeline
ADD ./common /common
WORKDIR /news_pipeline

CMD ["/bin/bash", "/news_pipeline/start.sh"]