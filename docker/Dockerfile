FROM ubuntu:16.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get -qq -y upgrade
RUN apt-get -qq -y install curl vim python2.7 python-dev python-pip python-virtualenv libmysqlclient-dev mysql-client
RUN pip install --upgrade pip
WORKDIR /src
COPY . ./
EXPOSE 8080

# RUN . env/bin/activate
# RUN ls -al
# RUN pip install --no-cache-dir pymysql
# RUN pip install --no-cache-dir mysqlclient
# RUN pip install --no-cache-dir --only-binary :all: grpcio
# RUN pip install --upgrade -r requirements.txt -t lib
# RUN ls -al docker
#RUN dev_appserver.py .
#ENV CLOUDSDK_PYTHON /src/env/bin/python
ENTRYPOINT ["/src/docker/docker-entrypoint.sh"]

# run migrations and start app
# CMD ["dev_appserver.py ."]

