#!/bin/bash

# # install GCP components
. env/bin/activate
apt-get -qq -y install apt-transport-https ca-certificates
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
apt-get update && apt-get -qq -y --force-yes install google-cloud-sdk google-cloud-sdk-app-engine-python google-cloud-sdk-app-engine-python-extras google-cloud-sdk-datastore-emulator
pip install --upgrade MySQL-python mysql-connector
pip install --upgrade -r requirements.txt -t lib
export CLOUDSDK_PYTHON=/usr/bin/python
apt-get -qq -y install google-cloud-sdk google-cloud-sdk-app-engine-python google-cloud-sdk-app-engine-python-extras

dev_appserver.py .
#ls -al
eval "$@"
