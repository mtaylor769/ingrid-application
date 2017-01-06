#!/bin/bash
mysql -udbuser -pMySQL123! -h 104.197.138.2  --ssl-ca=server-ca.pem --ssl-cert=client-cert.pem --ssl-key=client-key.pem
