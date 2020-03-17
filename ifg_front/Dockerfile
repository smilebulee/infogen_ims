# Pull python 3 image
FROM python:3

# Create a work dir
WORKDIR /usr/src/app

# copy requirements.txt into workdir created above
COPY requirements.txt ./

# Install all requirements
RUN python3 -m pip --trusted-host pypi.org --trusted-host files.pythonhosted.org install --user --no-cache-dir -r requirements.txt

# Copy entire project into workdir
COPY . .

EXPOSE 8000

# db 컨테이너 시작 여부 판단 툴
ENV DOCKERIZE_VERSION v0.2.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Run our app
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]