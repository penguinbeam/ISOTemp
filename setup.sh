sudo apt-get install python-requests
sudo apt-get install python-bluez

sudo /sbin/modprobe w1-gpio
sudo /sbin/modprobe w1-therm

On bluetooth receiving device make discoverable
sudo hciconfig hci0 piscan
