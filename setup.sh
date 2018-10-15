
sudo apt-get update
sudo apt-get install -y git
sudo git clone https://github.com/penguinbeam/ISOtemp

sudo apt-get install -y python-requests
sudo apt-get install -y python-bluez

#Install dependancy for the MI home trigger
sudo apt-get install python-requests

sudo /sbin/modprobe w1-gpio
sudo /sbin/modprobe w1-therm

echo "w1-gpio" | sudo tee -a /etc/modules
echo "w1-therm" | sudo tee -a /etc/modules

echo "dtoverlay=w1-gpio" | sudo tee -a /boot/config.txt

echo "These are your devices, if nothing shows reboot for the dtoverlay setting to take effect"
ls /sys/bus/w1/devices/ | grep -e "[0-9abcdef][0-9abcdef]-[0-9abcdef]\+"

sudo apt-get install -y supervisor
sudo cp /opt/ISOtemp/supervisord.conf.example /etc/supervisor/conf.d/isotemp.conf

echo "Find out BD Address for collecting server"
echo "sudo hciconfig hci0"
echo "On bluetooth receiving device make discoverable"
echo "sudo hciconfig hci0 piscan"


echo "Now edit your supervisor config isotemp.conf filling in the environment variables, remove the block not needed (IE no receiver on the logger, no transmitter on the receiver)"
