#!/bin/bash
ls -al
chmod 777 /var/lib/mysql
chown -R 1000:1000 /var/log/mysql
# mysqld --verbose --default-authentication-plugin=mysql_native_password --innodb-use-native-aio=0 --innodb-buffer-pool-size=20M
# chmod ug=rwx,o=rx  /var
# sudo chmod u=rwx,go=rx /var/log && \
# sudo chmod ug=rwx,o=rx /var/log/mysql && \
# sudo chmod -R ugo=rwx /var/lib/mysql && \
eval "$@"
