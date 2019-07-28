# 18부터는 python3 이 기본
FROM ubuntu:18.04

MAINTAINER OPEN-TUBE, "rhodochrosited@gmail.com"

# Ubuntu update 이 후 python, gcc등 소스코드 빌더 설치 
RUN apt-get update -y
RUN apt-get install -y build-essential
RUN apt-get install -y python python3 python3-dev python3-pip
RUN pip3 install --upgrade pip

ENV LANG C.UTF-8

# 소스코드 복사 및 작업 디렉토리 변경
COPY . /app
WORKDIR /app

# 패키지
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]


