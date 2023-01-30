#!/bin/bash
set -e

echo "----Variables initialization---"

srcDir="/home/pi/DemoInstall"
__PROJECT_NAME="RaspberryDemo"
__DIR_CODE_DESTINATION="/home/pi/${__PROJECT_NAME}"

# -- gateway : librairies installation
# verifie si les sources sont presentes. si non presente cela signifie que la gateway n a jamais ete installee.
if [ ! -d ${__DIR_CODE_DESTINATION} ];then
    echo "----Librairies installation---"
    apt-get update
    apt-get install -y python3
    apt-get install -y python3-pip
    apt-get install -y libxml2-dev 
    apt-get install -y libxslt-dev
    apt-get install -y python3-lxml
    apt-get install -y python3-dev
fi

echo "----Python packages installation---"
pip3 install smbus
pip3 install AWSIoTPythonSDK

echo "----Start installation---"
if [ -f /etc/systemd/system/main_acquisition.service ];then
    systemctl stop main_acquisition
fi

# clean previous installation
rm -rf ${__DIR_CODE_DESTINATION}

# scripts python3
if [ ! -d ${__DIR_CODE_DESTINATION} ];then
    echo "Folder creation !";
    mkdir ${__DIR_CODE_DESTINATION}
fi
cp -R ${srcDir}/* ${__DIR_CODE_DESTINATION}/.
rm -rf ${__DIR_CODE_DESTINATION}/services
rm -rf ${__DIR_CODE_DESTINATION}/docs
rm -rf ${__DIR_CODE_DESTINATION}/.??*

# services configuration
echo "----Authorizations configuration---"
cp -r ${srcDir}/* /etc/systemd/system/.

chmod -R 777 ${__DIR_CODE_DESTINATION}
chown root:root /etc/systemd/system/main_acquisition.service
chmod 777 /etc/systemd/system/main_acquisition.service

echo "----Activation services---"
systemctl enable main_acquisition

echo "----Start services---"
systemctl daemon-reload
systemctl start main_acquisition

echo "Show the services status"
systemctl | grep main
