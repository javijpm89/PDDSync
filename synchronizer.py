# -*- coding: utf-8 -*-

import configurator
import os
import hashlib
from termcolor import colored

# GETTING CONFIG ###

config = configurator.Configurator()

# END GETTING CONFIG #

# Functions

print " -- PDD SYNCHRONIZER V0.1 -- "

##
# Obtain Axon version from Axon_config files
##

with open(config.commander, 'r') as commander_file:
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

dir_services = os.listdir(config.path_services)
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
        myfile = os.listdir(config.path_services + mydir)
        if myfile.__len__() > 0:
            hasher.update(open(myfile[0]).read())
        else:
            pass
    digest = hasher.hexdigest()
    service_dictionary_hash.update({myfile: digest})


f_services = open(config.services_to_reload, 'w')

try:
    with open(config.services_md5_file, 'r') as s_file:
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
os.system('find ' + config.path_classes + ' -type f > ' + config.classes_temp_file)


dict_classes = {}
with open(config.classes_temp_file, 'r') as c_file:

    for line in c_file:
        if line is None:
            pass
        else:
            hasher.update('')
            hasher.update(open(config.path_classes + line).read())
            digest = hasher.hexdigest()
            dict_classes.update({config.path_classes + line: digest})

f_classes = open(config.classes_to_reload_file, 'rw')

with open(config.classes_md5_file, 'r') as c_md5_file:
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

with open(config.javauser_md5_file, 'r') as j_md5_file:
    line = j_md5_file.read()
    j_md5_from_file = line.split('-')[1]
    hasher.update(open(config.path_javauser).read())
    javauser_hash = hasher.hexdigest()



