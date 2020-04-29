# DockerHub에서 이미지 pull
FROM smilebulee/pyjava:0.3

# 받은 이미지의 /usr/src/app 경로로 이동
WORKDIR /usr/src/app

# 로컬의 dockerfile과 같은 경로에 있는 requirement.txt 파일을 이미지의 /usr/src/app 경로로 복사
COPY requirements.txt ./

# 복사한 requirement.txt 에 기술된 파이썬 모듈 설치
RUN python3 -m pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org install --user --no-cache-dir -r requirements.txt

# 로컬의 dockerfile과 같은 경로에 있는 모든 파일을 이미지의 /usr/src/app 경로로 복사
COPY . .

# 복사한 파일 중 docker-entrypoint.sh 에 실행권한을 줌
RUN chmod +x ./docker-entrypoint.sh
# 복사한 파일 중 docker-entrypoint.sh 을 실행
ENTRYPOINT ["./docker-entrypoint.sh"]