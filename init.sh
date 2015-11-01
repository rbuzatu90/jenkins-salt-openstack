#!/bin/bash

GIT_REPO=https://github.com/cloudbase/salt-openstack.git
SALT_OPENSTACK_DIR=/etc/salt/openstack
IP=`ifconfig | awk '/inet addr/{print substr($2,6)}' | grep -v 127.0.0.1`
HOSTNAME=`hostname`
ENVIRONMENT_FILES=$SALT_OPENSTACK_DIR/pillar_root/$ENVIRONMENT_NAME
ENVIRONMENT_NAME=$1

# Install salt minion
#sudo apt-get update && \
#sudo apt-get upgrade -y && \
sudo add-apt-repository ppa:saltstack/salt -y && \
sudo apt-get update && \
#sudo apt-get upgrade -y && \
sudo apt-get install salt-minion -y
sudo service salt-minion stop
sudo apt-get install git -y

git clone $GIT_REPO $SALT_OPENSTACK_DIR
if [ -d $SALT_OPENSTACK_DIR/pillar_root/$ENVIRONMENT_NAME ]; then
    echo "Environment dir already exists"
else
    cp -rf $SALT_OPENSTACK_DIR/pillar_root/samples/single_nic $SALT_OPENSTACK_DIR/pillar_root/$ENVIRONMENT_NAME
fi
echo $HOSTNAME > /etc/salt/minion_id

cat << FINISH > $SALT_OPENSTACK_DIR/../minion
file_client: local
pillar_roots:
  openstack:
    - $SALT_OPENSTACK_DIR/pillar_root
file_roots:
  openstack:
    - $SALT_OPENSTACK_DIR/file_root
jinja_trim_blocks: True
jinja_lstrip_blocks: True
FINISH

sed -i "s/<minion_id_1>,<minion_id_2>/$HOSTNAME/g" $SALT_OPENSTACK_DIR/pillar_root/top.sls
sed -i "s/<openstack_environment_name>/$ENVIRONMENT_NAME/g" $SALT_OPENSTACK_DIR/pillar_root/top.sls

sed -i "s/ubuntu.openstack/$HOSTNAME/g" $SALT_OPENSTACK_DIR/pillar_root/$ENVIRONMENT_NAME/networking.sls

sed -i "s/ubuntu.openstack/$HOSTNAME/g" $SALT_OPENSTACK_DIR/pillar_root/$ENVIRONMENT_NAME/environment.sls
sed -i "s/192.168.137.71/$IP/g" $SALT_OPENSTACK_DIR/pillar_root/$ENVIRONMENT_NAME/environment.sls

