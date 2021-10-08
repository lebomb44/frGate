# Update the operating system
```
jeedom@jeedom:~$ sudo apt update
```

#######################################################
# Shell In A Box
```shell
jeedom@osjeedommc:~$ sudo apt install shellinabox
```
# Edit the file 
```shell
jeedom@jeedom:~$ sudo vi /etc/default/shellinabox
```
# Add a "-t" at the end of the last line:
```shell
SHELLINABOX_ARGS="--no-beep -t"
```
# Reboot to test that the service a started and listen on port 4200
# Open a web navigator on port 4200

#######################################################
# Nginx
```shell
jeedom@jeedom:~$ sudo apt install nginx-extras
```
# Copy the file "default" in this folder
```shell
osmc@osmc:~$ cd /etc/nginx/sites-available/
```
# Create html folder
# Copy the file "default" in this folder
```shell
osmc@osmc:/etc/nginx/html$ cd /etc/nginx/
osmc@osmc:/etc/nginx$ sudo mkdir html
```
# Go to HTML folder
```shell
osmc@osmc:/etc/nginx$ cd html
```
# Copy "index.html", "favicon.png" and folder "css"
# Create authentification file
```shell
osmc@osmc:/etc/nginx/html$ cd /etc/nginx/
osmc@osmc:/etc/nginx$ sudo htpasswd -c .htpasswd user1
osmc@osmc:/etc/nginx$ sudo htpasswd .htpasswd user2
```
# Edit NGINX configuration file to allow big file upload
```shell
osmc@osmc:~$ sudo vi /etc/nginx/nginx.conf
```
# Add the following line:
```shell
        client_max_body_size 100000M;
        server_tokens off;
```
# Reboot
```shell
osmc@osmc:/etc/nginx$ sudo reboot
