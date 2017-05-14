FROM python:2.7

MAINTAINER shi.tianhao.sth@gmail.com
# http://mirrors.aliyun.com/pypi/simple/
# https://pypi.tuna.tsinghua.edu.cn/simple

ADD ./config.yaml /

RUN pip install --upgrade setuptools -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

ADD ./web_server/backend_server /backend_server
ADD ./common /common

WORKDIR /backend_server

CMD ["/bin/bash", "/backend_server/start.sh"]