#!/usr/bin/env python

# Requirements:
# Watchdog: pip install watchdog
# PyCrypto: http://www.voidspace.org.uk/python/modules.shtml#pycrypto
# Paramiko: pip install paramiko

import sys, os, time
from watchdog.observers import Observer
from handlers import WotcherEventHandler
from sync import SFTPSync


host = 'foo'
username = 'bar'
password = 'baz'

sftp_syncer = SFTPSync(host, username, password)

# local, remote
sftp_syncer.add_dir("/home/something", "/var/www/something")


event_handler = WotcherEventHandler(sftp_syncer.modified)
observer = Observer()

print ""
print "********************************************************************************"
print "                                WOTCHER                                         "
print "                             Ctrl+C to exit                                     "
print "********************************************************************************"
print ""

sftp_syncer.connect()

for directory in sftp_syncer.dirs:
	print "+ {0} -> {1}".format(directory[0], directory[1])
	observer.schedule(event_handler, directory[0], recursive=True)

print ""
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    sftp_syncer.close()
observer.join()
