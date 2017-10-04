# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser
import os
import hashlib
from termcolor import colored

# GETTING CONFIG ###

configfile = 'config.ini'
config = SafeConfigParser()
config.read(configfile)

## Paths
path_axon_home = config.get('path', 'axon_home')
path_services = path_axon_home + config.get('path', 'axon_relative_services')
path_javauser = path_axon_home + config.get('path', 'axon_relative_javauser') + 'javauser.jar'
path_libs = path_axon_home + config.get('path', 'axon_relative_libs')
path_classes = path_axon_home + config.get('path', 'axon_relative_classes')
commander = path_axon_home + 'engine/' + config.get('files', 'axon_commander')
sync_home = config.get('path', 'synchronizer_home')

## Adresses and ports
# Primary node
ax_primary_node = config.get('primary_node','address')
ax_primary_port = config.get('primary_node', 'port')

# Secondary node
ax_primary_node = config.get('secondary_node','address')
ax_secondary_port = config.get('secondary_node', 'port')

## Files
# Services files
services_md5_file = config.get('files', 'serviceschecksumfile')
services_to_reload = config.get('files', 'servicestoreload')

# Classes files
classes_md5_file = config.get('files', 'classeschecksumfile')
classes_to_reload_file = config.get('files', 'classestoreload')
classes_temp_file = config.get('files', 'temp_file')

# Javauser files
javauser_md5_file = config.get('files', 'javauser_checksum_file')

## Reloaders
# Javauser
ju_reloader = sync_home + config.get('scripts','javauser_reloader')

# END GETTING CONFIG #

# Functions


def reloadjavauser(port, jaxon):
    os.system(sync_home + ju_reloader + ' ' + port + ' ' + jaxon)


print " -- PDD SYNCHRONIZER V0.1 -- "

##
# Obtain Axon version from Axon_config files
##

with open(commander, 'r') as commander_file:
    for line in commander_file.readlines:
        if 'jaxon' not in line:
            pass
        else:
            line_splitted = line.split('/')
            for entry in line_splitted:
                if str(entry).startswith('jaxon'):
                    axon_version = str(entry).split(' ')[0]
                else:
                    pass


print "Analyzing Axón Services"

dir_services = os.listdir(path_services)
dir_services.__len__()

service_dictionary_hash = {}

print "Getting md5hash from current files"

hasher = hashlib.md5()


##
# Services
##

for mydir in dir_services:
    hasher.update('')

    if mydir.endswith('xml'):
        myfile = mydir
        hasher.update(open(myfile).read())
    else:
        myfile = os.listdir(path_services + mydir)
        if myfile.__len__() > 0:
            hasher.update(open(myfile[0]).read())
        else:
            pass
    digest = hasher.hexdigest()
    service_dictionary_hash.update({myfile: digest})


f_services = open(services_to_reload, 'w')

try:
    with open(services_md5_file, 'r') as s_file:
        for line in s_file.readlines:
            service_file = line.split('-')[0]
            service_hash_file = line.split('-')[1]
            service_hash = service_dictionary_hash.get(service_file)

            if service_hash == service_hash_file:
                print colored("Service " + str(service_file) + "has not changed",'green')
            else:
                print colored("Service " + str(service_file) + "has changed. Adding to list to reload and synchronize", 'yellow')
                f_services.write(service_file)
                f_services.write('\n')
except Exception as e:
    print e.message
finally:
    f_services.close()

##
# Classes
##

print "Analyzing Web Service Classes"
# Using find to discover all classes recursively
os.system('find ' + path_classes + ' -type f > ' + classes_temp_file)


dict_classes = {}
with open(classes_temp_file, 'r') as c_file:

    for line in c_file:
        if line is None:
            pass
        else:
            hasher.update('')
            hasher.update(open(path_classes + line).read())
            digest = hasher.hexdigest()
            dict_classes.update({path_classes + line: digest})

f_classes = open(classes_to_reload_file, 'rw')

with open(classes_md5_file, 'r') as c_md5_file:
    for line in c_md5_file:
        class_file = line.split('-')[0]
        class_hash_from_file = line.split('-')[1]
        class_hash = dict_classes.get(class_file)

        if class_hash_from_file == class_hash:
            print colored('Class ' + str(class_file) + 'has not changed', 'green')
        else:
            print colored('Class' + str(class_file) + 'has changed. Adding to list to reload and synchronize','yellow')
            f_classes.write(class_file)
            f_classes.write('\n')


print "Analyzing Javauser"

with open(javauser_md5_file,'r') as j_md5_file:
    line = j_md5_file.read()
    j_md5_from_file = line.split('-')[1]
    hasher.update(open(path_javauser).read())
    javauser_hash = hasher.hexdigest()



