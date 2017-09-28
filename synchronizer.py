# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser
import os
import hashlib
from termcolor import colored

# GETTING CONFIG ###

configfile = 'config.ini'
config = SafeConfigParser()
config.read(configfile)

path_axon_home = config.get('path', 'axon_home')

path_services = path_axon_home + config.get('path', 'axon_relative_services')
path_javauser = path_axon_home + config.get('path', 'axon_relative_javauser')
path_libs = path_axon_home + config.get('path', 'axon_relative_libs')
path_classes = path_axon_home + config.get('path', 'axon_relative_classes')

services_md5_file = config.get('files', 'serviceschecksumfile')
services_reload_file_config = config.get('files', 'servicestoreload')
classes_temp_file = config.get('files', 'temp_file')

# END GETTING CONFIG #

print " -- PDD SYNCHRONIZER V0.1 -- "

print "Analyzing Axón Services"

dir_services = os.listdir(path_services)
dir_services.__len__()

service_dictionary_hash = {}

print "Getting md5hash from current files"


hasher = hashlib.md5()

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

f_services = open(services_reload_file_config, 'rw+')

with open(services_md5_file, 'r') as sfile:
    for line in sfile.readlines:
        service_file = line.split('-')[0]
        service_hash_file = line.split('-')[1]
        service_hash= service_dictionary_hash.get(service_hash_file)

        if service_hash == service_hash_file:
            print colored("Service " + str(service_file) + "has not changed",'green')
        else:
            print colored("Service " + str(service_file) + "has changed. Adding to list to reload and synchronize",'yellow')
            f_services.write(service_file)
            f_services.write('\n')

f_services.close()

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
            hasher.update(line)
            digest = hasher.hexdigest()
            dict_classes.update({line: digest})
