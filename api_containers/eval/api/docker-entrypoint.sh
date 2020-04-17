#!/bin/bash

python3 -u app.py &
java -Dspring.application.name="eval-api" -Deureka.serverUrl="host.docker.internal" -Deureka.serverPort=8761 -Dsidecar.hostname="localhost" -Dsidecar.port=5007 -jar sidecar-0.0.1-SNAPSHOT.jar
