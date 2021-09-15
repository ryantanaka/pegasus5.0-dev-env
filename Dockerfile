# Ubuntu 18.04
from nvidia/cuda:10.1-base

# install linux packages
RUN apt update && apt install -y \
        software-properties-common \
        wget \
        curl \
        sudo \
        vim \
        default-jre


# set locale
ENV LANG C.UTF-8

# user setup (pw: scitech123)
RUN groupadd --gid 808 scitech-group
RUN useradd --gid 808 --uid 550 --create-home --password '$6$ouJkMasm5X8E4Aye$QTFH2cHk4b8/TmzAcCxbTz7Y84xyNFs.gqm/HWEykdngmOgELums1qOi3e6r8Z.j7GEA9bObS/2pTN1WArGNf0' scitech
RUN usermod -aG sudo scitech
RUN echo "scitech ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Docker + Docker in Docker setup
RUN curl -sSL https://get.docker.com/ | sh
ADD ./config/wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker
VOLUME /var/lib/docker
RUN usermod -aG docker scitech

# install python and required packages
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install -y python3.7 python3-pip
RUN pip3 install pyyaml GitPython jupyter

# install htcondor
RUN wget -qO - https://research.cs.wisc.edu/htcondor/ubuntu/HTCondor-Release.gpg.key | sudo apt-key add -
RUN echo "deb http://research.cs.wisc.edu/htcondor/ubuntu/8.8/bionic bionic contrib" >> /etc/apt/sources.list
RUN echo "deb-src http://research.cs.wisc.edu/htcondor/ubuntu/8.8/bionic bionic contrib" >> /etc/apt/sources.list
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y htcondor

# configure minihtcondor and GPU usage
RUN wget -O /etc/condor/config.d/00-minicondor-ubuntu https://raw.githubusercontent.com/htcondor/htcondor/master/build/docker/services/mini/00-minicondor-ubuntu
RUN echo "use feature : GPUs" >> /etc/condor/condor_config

# install pegasus
RUN wget "https://download.pegasus.isi.edu/pegasus/development/5.1/ubuntu/dists/bionic/main/binary-amd64/pegasus_5.1.0~dev202109142128-1+ubuntu18_amd64.deb" \
    && apt install -y ./pegasus_5.1.0~dev202109142128-1+ubuntu18_amd64.deb \
    && rm -f pegasus_5.1.0~dev202109142128-1+ubuntu18_amd64.deb


# tests
RUN python3 -c "print('python tēst working')"

# setup entrypoint
# TODO: figure out why condor_master doesn't start if I do it this way...
ENV EP /usr/local/bin/entrypoint.sh
RUN echo "#!/bin/bash" >> $EP \
    && chmod u+x $EP \
    && printf "\ncondor_master\n" >> $EP \
    && tail -n 113 /usr/local/bin/wrapdocker >> $EP

# user setup
USER scitech
WORKDIR /home/scitech

RUN echo "export PYTHONPATH=$(pegasus-config --python)" >> ~/.bashrc

# setup configuration for ensemble manager
RUN pegasus-db-admin create
RUN printf "#!/usr/bin/env python3\nUSERNAME='scitech'\nPASSWORD='scitech123'\n" >> /home/scitech/.pegasus/service.py \
    && chmod u+x /home/scitech/.pegasus/service.py

# Set notebook password to 'scitech'. This pw will be used instead of token authentication
RUN mkdir /home/scitech/.jupyter \ 
    && echo "{ \"NotebookApp\": { \"password\": \"sha1:30a323540baa:6eec8eaf3b4e0f44f2f2aa7b504f80d5bf0ad745\" } }" >> /home/scitech/.jupyter/jupyter_notebook_config.json

ENTRYPOINT ["sudo", "/usr/local/bin/entrypoint.sh"]
CMD ["su", "-", "scitech", "-c", "jupyter notebook --notebook-dir=/home/scitech/shared-data --port=8888 --no-browser --ip=0.0.0.0 --allow-root"] 
