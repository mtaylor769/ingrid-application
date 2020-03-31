#!/bin/bash -e
# run as root
# sudo -i
# echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections

# update package list
sudo apt-get -qq -y update && sudo apt-get -qq -y upgrade
sudo apt-get -qq -y install --reinstall update-manager-core
sudo apt-get -qq -y install --install-recommends linux-generic-lts-xenial
# sudo do-release-upgrade -y

# install some essentials
sudo apt-get -qq -y install apt-utils g++ build-essential git-core curl bash vim jq apt-transport-https ca-certificates mysql-client bridge-utils
# # install docker compose
wget -qO- https://get.docker.com/ | sh

sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" > docker-compose
sudo mv docker-compose /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo apt-get -y --force-yes install docker-ce=18.06.1~ce~3-0~ubuntu
# make docker daemon available to the vagrant user
sudo gpasswd -a ${USER} docker
sudo service docker restart

# install Java 8
sudo add-apt-repository ppa:openjdk-r/ppa &&
sudo apt-get -qq -y update &&
sudo apt-get -qq -y install openjdk-8-jdk

# cleanup
sudo apt-get -qq -y autoremove

# # install unicreds
# cd /home/vagrant
# wget https://github.com/Versent/unicreds/releases/download/v1.5.0/unicreds_1.5.0_linux_x86_64.tgz
# tar xzvf unicreds_1.5.0_linux_x86_64.tgz
# chmod +x unicreds
# sudo mv unicreds /usr/local/bin/

# install nvm
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.32.1/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm

# install node
nvm i 6

# setup shared network
sudo docker network create localnet

# cd to /vagrant by default
echo "cd /vagrant" >> /home/vagrant/.bashrc

# copy docker utility scripts
sudo cp /vagrant/scripts/dev.sh /usr/local/bin/dev
sudo cp /vagrant/scripts/run.sh /usr/local/bin/run
sudo chmod +x /usr/local/bin/dev
sudo chmod +x /usr/local/bin/run

