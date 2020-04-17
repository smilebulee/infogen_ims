#!/bin/bash

python3 -u app.py &
java -Deureka.serverUrl="host.docker.internal" -Deureka.serverPort=8761 -Dsidecar.url="localhost" -Dsidecar.port=5009 -jar sidecar-0.0.1-SNAPSHOT.jar
