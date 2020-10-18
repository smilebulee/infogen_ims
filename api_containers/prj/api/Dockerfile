# Pull python 3 image
FROM smilebulee/pyjava:0.3

# Create a work dir
WORKDIR /usr/src/app

# copy requirements.txt into workdir created above
COPY requirements.txt ./

# Install all requirements
RUN python3 -m pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org install --user --no-cache-dir -r requirements.txt

# Copy entire project into workdir
COPY . .
RUN chmod +x ./docker-entrypoint.sh
# Run our app
#CMD ["python", "app.py"]
ENTRYPOINT ["./docker-entrypoint.sh"]