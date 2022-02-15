# Update the operating system
```
jeedom@jeedom:~$ sudo apt update
jeedom@jeedom:~$ sudo apt full-upgrade
```

#######################################################
# Shell In A Box
```shell
jeedom@jeedom:~$ sudo apt install shellinabox
```
## Edit the file 
```shell
jeedom@jeedom:~$ sudo vi /etc/default/shellinabox
jeedom@jeedom:~$ sudo /etc/init.d/shellinabox stop
```
## Add a "-t" at the end of the last line:
```shell
SHELLINABOX_ARGS="--no-beep -t"
```
## Reboot to test that the service a started and listen on port 4200
## Open a web navigator on port 4200

#######################################################
# Change Apache2 default ports
```shell
jeedom@osjeedom:~$ sudo vi /etc/apache2/ports.conf
Listen 8080
Listen 444
Listen 444
```

#######################################################
# Nginx
```shell
jeedom@jeedom:~$ sudo apt install nginx-extras fcgiwrap php-fpm
```
## Copy the file "default" in this folder
```shell
jeedom@jeedom:~$ cd /etc/nginx/sites-available/
```
## Create html folder
```shell
jeedom@jeedom:/etc/nginx/html$ cd /etc/nginx/
jeedom@jeedom:/etc/nginx$ sudo mkdir html
```
## Go to HTML folder
```shell
jeedom@jeedom:/etc/nginx$ cd html
```
## Copy "index.html", "favicon.png" and folder "css"
## Create authentification file
```shell
jeedom@jeedom:/etc/nginx/html$ cd /etc/nginx/
jeedom@jeedom:/etc/nginx$ sudo htpasswd -c .htpasswd user1
jeedom@jeedom:/etc/nginx$ sudo htpasswd .htpasswd user2
```
## Edit NGINX configuration file to allow big file upload
```shell
jeedom@jeedom:~$ sudo vi /etc/nginx/nginx.conf
```
## Add the following line:
```shell
        client_max_body_size 100000M;
        server_tokens off;
	more_clear_headers Server;
	#access_log /var/log/nginx/access.log;
	access_log off;
	#error_log /var/log/nginx/error.log;
	error_log off;
```
#######################################################
# Check services
```shell
jeedom@jeedom:~$ sudo su -
root@jeedom:~$ crontab -e
0 * * * * /home/jeedom/frGate/nginx/check-services.sh > /tmp/check-services.log
```
#######################################################
# Install lbGate
```shell
jeedom@frdom:~/frGate/service $ sudo cp lbGate /etc/init.d/.
jeedom@frdom:~/frGate/service $ sudo update-rc.d lbGate defaults
jeedom@frdom:~/frGate/service $ cd
jeedom@frdom:~ $ sudo apt install rpi.gpio
jeedom@frdom:~ $ ln -s /home/jeedom/frGate/lbGate.py lbGate.py
```
#######################################################
# Static IP
```shell
jeedom@frdom:~/frGate $ sudo vi /etc/dhcpcd.conf
# Example static IP configuration:
interface eth0
static ip_address=192.168.10.4/24
#static ip6_address=fd51:42f8:caae:d92e::ff/64
static routers=192.168.10.1
static domain_name_servers=8.8.8.8
```
#######################################################
# Reboot
```shell
jeedom@frdom:~ $ sudo reboot
```
#######################################################
# Read DS18B20 temperature
```shell
jeedom@frdom:~ $ find /sys/bus/w1/devices/ -name "28-*" -exec cat {}/w1_slave \; | grep "t=" | awk -F "t=" '{print $2/1000}'
```
#######################################################
# ConBee 2 firmware upgrade on Ubuntu
Source : http://ronhks.hu/2021/04/22/conbee-2-firmware-upgrade-on-ubuntu/
Requirements:
Installed Deconz software. Downloadable, here: http://deconz.dresden-elektronik.de/ubuntu/stable/
Download the lates firmware from here:
http://deconz.dresden-elektronik.de/deconz-firmware/?C=M;O=D
(deCONZ_ConBeeII_0x)

Stop all services:
```shell
$ sudo systemctl stop deconz && sudo systemctl stop deconz-gui
```
Stop ModemManager if it is installed:
```shell
$ sudo systemctl stop ModemManager
```
Update the firmware:
```shell
sudo GCFFlasher_internal -t 60 -d /dev/ttyACM0 -f <LOCATION_OF_THE FIRMWARE_IMG>/deCONZ_ConBeeII_0x1234567.bin.GCF
```
src: https://github.com/dresden-elektronik/deconz-rest-plugin/wiki/Update-deCONZ-manually
