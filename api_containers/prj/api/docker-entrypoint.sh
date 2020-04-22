#!/bin/bash

python3 -u app.py &
java -Dspring.profiles.active=${SPRING_PROFILES_ACTIVE} -Dspring.application.name=${SPRING_APPLICATION_NAME} -Dsidecar.port=${SIDECAR_PORT} -jar sidecar-0.0.1-SNAPSHOT.jar
