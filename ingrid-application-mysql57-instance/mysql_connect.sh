#!/bin/bash
mysql -udbuser -pMySQL123! -h127.0.0.1  --ssl-ca=server-ca.pem --ssl-cert=client-cert.pem --ssl-key=client-key.pem
