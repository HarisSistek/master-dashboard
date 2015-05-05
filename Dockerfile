FROM centos
ENV BASE /opt/website
ENV ENV /opt/website/env/
ENV PYTHON /opt/website/env/bin/python

RUN yum clean all && yum install -y python-virtualenv python-pip
ADD requirements.txt $BASE/requirements.txt
RUN cd $BASE && virtualenv env
RUN $ENV/bin/pip install -r $BASE/requirements.txt

EXPOSE 10000
CMD /opt/website/env/bin/python /opt/website/run.py
