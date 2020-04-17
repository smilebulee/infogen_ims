#!/bin/bash

python3 -u app.py &
java -Dspring.application.name="site-api" -Deureka.serverUrl="host.docker.internal" -Deureka.serverPort=8761 -Dsidecar.url="localhost" -Dsidecar.port=5010 -jar sidecar-0.0.1-SNAPSHOT.jar
