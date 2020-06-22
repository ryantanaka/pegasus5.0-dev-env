FROM centos:centos7

RUN yum -y update | /bin/true

RUN groupadd --gid 808 scitech-group
RUN useradd --gid 808 --uid 550 --create-home --password '$6$ouJkMasm5X8E4Aye$QTFH2cHk4b8/TmzAcCxbTz7Y84xyNFs.gqm/HWEykdngmOgELums1qOi3e6r8Z.j7GEA9bObS/2pTN1WArGNf0' scitech

# Configure Sudo
RUN echo -e "scitech ALL=(ALL)       NOPASSWD:ALL\n" >> /etc/sudoers

# Test requirements
RUN yum -y install epel-release
RUN yum -y install ant | /bin/true
RUN yum -y install \
     ant-apache-regexp \
     ant-junit \
     bc \
     bzip2-devel \
     ca-certificates \ 
     cryptsetup \
     epel-release \
     gcc \
     gcc-c++ \
     git \
     golang \
     iptables \ 
     java-1.8.0-openjdk-devel \
     libffi-devel \
     libseccomp-devel \
     libuuid-devel \
     lxc \
     make \
     mpich-devel \
     mysql-devel \
     openssl-devel \
     patch \
     postgresql-devel \
     python36-devel \
     python36-pip \
     python36-pyOpenSSL \
     python36-pytest \
     python36-PyYAML \
     python36-setuptools \
     R-devel \
     readline-devel \
     rpm-build \
     singularity \
     sqlite-devel \
     sudo \ 
     squashfs-tools \
     tar \
     vim \ 
     wget \
     which \
     yum-plugin-priorities \
     zlib-devel 

# Docker + Docker in Docker setup
RUN curl -sSL https://get.docker.com/ | sh
ADD ./config/wrapdocker /usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker

VOLUME /var/lib/docker

RUN usermod -aG docker scitech

# Python test requirements - FIXME: not a great idea to use pip3 install in this container
RUN pip3 install tox

# Documentation - FIXME: not a great idea to use pip3 install in this container
RUN pip3 install six sphinx recommonmark sphinx_rtd_theme sphinxcontrib-openapi javasphinx jupyter

# Set Timezone
RUN cp /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

# Get Condor yum repo
RUN curl -o /etc/yum.repos.d/condor.repo https://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo
RUN rpm --import https://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor
RUN yum -y install condor minicondor
RUN sed -i 's/condor@/scitech@/g' /etc/condor/config.d/00-minicondor

RUN usermod -a -G condor scitech
RUN chmod -R g+w /var/{lib,log,lock,run}/condor

RUN chown -R scitech /home/scitech/

RUN echo -e "condor_master > /dev/null 2>&1" >> /home/scitech/.bashrc

USER scitech

WORKDIR /home/scitech

# Set up config for ensemble manager
RUN mkdir /home/scitech/.pegasus \
    && echo -e "#!/usr/bin/env python3\nUSERNAME='scitech'\nPASSWORD='scitech123'\n" >> /home/scitech/.pegasus/service.py \
    && chmod u+x /home/scitech/.pegasus/service.py

# Set ARG on build so that we can pull latest pegasus 
ARG BUILD_DATE=2020-06-01_12:59:18

# Get Pegasus master
RUN git clone https://github.com/pegasus-isi/pegasus.git \
    && cd pegasus \
    && ant dist

ENV PATH /home/scitech/pegasus/dist/pegasus-5.0.0dev/bin:$HOME/.pyenv/bin:$PATH:/usr/lib64/mpich/bin
ENV PYTHONPATH /home/scitech/pegasus/dist/pegasus-5.0.0dev/lib64/python3.6/site-packages

# Set up pegasus database
RUN /home/scitech/pegasus/dist/pegasus-5.0.0dev/bin/pegasus-db-admin update sqlite:////home/scitech/.pegasus/workflow.db

# Set Kernel for Jupyter (exposes PATH and PYTHONPATH for use when terminal from jupyter is used)
ADD ./config/kernel.json /usr/local/share/jupyter/kernels/python3/kernel.json
RUN echo -e "export PATH=/home/scitech/pegasus/dist/pegasus-5.0.0dev/bin:/home/scitech/.pyenv/bin:\$PATH:/usr/lib64/mpich/bin" >> /home/scitech/.bashrc
RUN echo -e "export PYTHONPATH=/home/scitech/pegasus/dist/pegasus-5.0.0dev/lib64/python3.6/site-packages" >> /home/scitech/.bashrc

ENTRYPOINT ["sudo", "/usr/local/bin/wrapdocker"]
CMD ["su", "-", "scitech", "-c", "jupyter notebook --notebook-dir=/home/scitech/shared-data --port=8888 --no-browser --ip=0.0.0.0 --allow-root"] 
