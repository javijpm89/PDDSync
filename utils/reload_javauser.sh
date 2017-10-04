#!/bin/bash
# /vt1/scripts/utils/

PORT= $1
JAXON= $2

export JAVA_HOME=/usr/local/java
export PATH=/usr/local/java/bin:$PATH

echo Recargando wsclasses...
java -classpath "/vtjar/dweb/jaxon_v9.1.250.jar" es.brainwave.utils.AxonCommander monitor 127.0.0.1 9870 << IN
wsclasses
userclasses
exit
IN