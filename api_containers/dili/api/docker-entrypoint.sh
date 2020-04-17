#!/bin/bash

python3 -u app.py &
java -Dspring.application.name="dili-api" -Deureka.serverUrl="host.docker.internal" -Deureka.serverPort=8761 -Dsidecar.url="localhost" -Dsidecar.port=5006 -jar sidecar-0.0.1-SNAPSHOT.jar
