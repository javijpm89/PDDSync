# -*- coding: utf-8 -*-
import os
from termcolor import colored


def reloadjavauserandwsclasses(port, reloader):
    print colored("Reloading javauser and wsclasses on port " + port, 'green')
    os.system(reloader)


def reloadservices(port, reloader):
    print colored("Reloading services on port " + port, 'green')
    os.system(reloader)