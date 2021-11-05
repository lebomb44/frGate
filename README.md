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
jeedom@jeedom:~$ sudo apt install nginx-extras fcgiwrap
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
jeedom@jeedom:/etc/nginx$ sudo reboot
```
#######################################################
