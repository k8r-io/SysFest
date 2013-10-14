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
import sys

site.addsitedir('/var/www/sysfest/venv/lib/python2.6/site-packages')
os.environ['SYSFEST_CONFIG'] = '/var/www/sysfest/sysfest.conf'

sys.path.append('/var/www/sysfest/')
import monitor
monitor.start(interval=1.0)
from sysfest import app as application" | tee /var/www/sysfest/sysfest.wsgi

mkdir -p /var/www/sysfest/monitor

echo "import os
import sys
import time
import signal
import threading
import atexit
import Queue

_interval = 1.0
_times = {}
_files = []

_running = False
_queue = Queue.Queue()
_lock = threading.Lock()

def _restart(path):
    _queue.put(True)
    prefix = 'monitor (pid=%d):' % os.getpid()
    print >> sys.stderr, '%s Change detected to \'%s\'.' % (prefix, path)
    print >> sys.stderr, '%s Triggering process restart.' % prefix
    os.kill(os.getpid(), signal.SIGINT)

def _modified(path):
    try:
        # If path doesn't denote a file and were previously
        # tracking it, then it has been removed or the file type
        # has changed so force a restart. If not previously
        # tracking the file then we can ignore it as probably
        # pseudo reference such as when file extracted from a
        # collection of modules contained in a zip file.

        if not os.path.isfile(path):
            return path in _times

        # Check for when file last modified.

        mtime = os.stat(path).st_mtime
        if path not in _times:
            _times[path] = mtime

        # Force restart when modification time has changed, even
        # if time now older, as that could indicate older file
        # has been restored.

        if mtime != _times[path]:
            return True
    except:
        # If any exception occured, likely that file has been
        # been removed just before stat(), so force a restart.

        return True

    return False

def _monitor():
    while 1:
        # Check modification times on all files in sys.modules.

        for module in sys.modules.values():
            if not hasattr(module, '__file__'):
                continue
            path = getattr(module, '__file__')
            if not path:
                continue
            if os.path.splitext(path)[1] in ['.pyc', '.pyo', '.pyd']:
                path = path[:-1]
            if _modified(path):
                return _restart(path)

        # Check modification times on files which have
        # specifically been registered for monitoring.

        for path in _files:
            if _modified(path):
                return _restart(path)

        # Go to sleep for specified interval.

        try:
            return _queue.get(timeout=_interval)
        except:
            pass

_thread = threading.Thread(target=_monitor)
_thread.setDaemon(True)

def _exiting():
    try:
        _queue.put(True)
    except:
        pass
    _thread.join()

atexit.register(_exiting)

def track(path):
    if not path in _files:
        _files.append(path)

def start(interval=1.0):
    global _interval
    if interval < _interval:
        _interval = interval

    global _running
    _lock.acquire()
    if not _running:
        prefix = 'monitor (pid=%d):' % os.getpid()
        print >> sys.stderr, '%s Starting change monitor.' % prefix
        _running = True
        _thread.start()
    _lock.release() " | tee /var/www/sysfest/monitor/__init__.py

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
    EnableSendfile Off
</VirtualHost>" | tee /etc/httpd/conf.d/sysfest.conf

service httpd restart
chkconfig httpd on
service mongod restart
chkconfig mongod on
service iptables stop
chkconfig iptables off
