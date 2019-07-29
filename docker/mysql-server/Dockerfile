FROM mariadb/server

RUN chmod 777 /var/lib/mysql
COPY ./test.sql /docker-entrypoint-initdb.d
RUN echo "1000  ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers
RUN echo "mysql  ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers
RUN chown -R 1000:1000 /var/log/mysql
USER 1000

# EXPOSE 3306
# ENTRYPOINT [ "docker-entrypoint.sh" ]
# CMD [ "mysqld", "--verbose"]
