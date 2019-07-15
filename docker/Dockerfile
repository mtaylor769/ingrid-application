FROM python:2.7.15-jessie
VOLUME /app
COPY . /app
WORKDIR /app
EXPOSE 8080
RUN ls -al
#RUN apt-get -qq -y install python-dev python-pip python-virtualenv libmysqlclient-dev mysql-server
RUN pip install --upgrade pip
RUN . env/bin/activate
# RUN ls -al
# RUN pip install --no-cache-dir pymysql
# RUN pip install --no-cache-dir mysqlclient
# RUN pip install --no-cache-dir --only-binary :all: grpcio
RUN pip install --upgrade -r requirements.txt -t lib
#RUN dev_appserver.py .
ENV CLOUDSDK_PYTHON /app/env/bin/python
ENTRYPOINT ["python"]
CMD ["/bin/bash", "-e", "cd /app"]
