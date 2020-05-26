FROM python:3.7
COPY ./docker_config/pip.conf /etc/pip.conf
#COPY ./docker_config/sources.list /etc/apt/sources.list
WORKDIR /opt/apps
ADD requirements.txt ./requirements.txt 
RUN apt-get update
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
ENV LC_ALL='C.UTF-8'
RUN useradd guo -m
COPY  code /opt/projects/
RUN chown -R guo:guo /opt/projects
USER guo
