#!/bin/bash

echo "[mongodb]
name=MongoDB Repository
baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64/
gpgcheck=0
enabled=1" | tee /etc/yum.repos.d/10gen.repo

rpm -Uhv http://mirror.vcu.edu/pub/gnu+linux/epel/6/i386/epel-release-6-8.noarch.rpm
yum -y install httpd mod_wsgi git vim-enahnces python python-virtualenv mongo-10gen-server  mongo-10gen


mkdir /var/www/sysfest
ln -s /vagrant/angular-sysfest/ /var/www/sysfest/angular-sysfest

virtualenv /var/www/sysfest/venv
. /var/www/sysfest/venv/bin/activate
pip install -e /vagrant/SysFest

echo "import site
import os
site.addsitedir('/var/www/sysfest/venv/lib/python2.6/site-packages')
from sysfest import app as application" | tee /var/www/sysfest/sysfest.wsgi

echo "<VirtualHost *:80>
    ServerName sysfest.local
    ServerAlias localhost

    DocumentRoot /var/www/sysfest/angular-sysfest/app

    WSGIDaemonProcess sysfest user=apache group=apache
    WSGIScriptAlias /api /var/www/sysfest/sysfest.wsgi
    <Directory /var/www/sysfest/venv>
        WSGIProcessGroup sysfest
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>

</VirtualHost>" | tee /etc/httpd/conf.d/sysfest.conf

service httpd restart
service mongod restart

iptables -F
