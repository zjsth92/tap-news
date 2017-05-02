FROM jupyter/scipy-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>
# install python2 tensorflow
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ & conda config --set show_channel_urls yes
RUN conda install --quiet --yes -n python2 'tensorflow=1.0.1'
