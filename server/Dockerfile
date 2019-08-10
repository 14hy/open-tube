
MAINTAINER OPEN-TUBE, "rhodochrosited@gmail.com"

# Ubuntu update 이 후 python, gcc등 소스코드 빌더 설치
RUN apt-get update -y
RUN apt-get install -y build-essential
RUN apt-get install -y python python3 python3-dev python3-pip

# C library, PostgreSQL interface dependency
RUN apt-get install -y libpq-dev
RUN pip3 install --upgrade pip

ENV LANG C.UTF-8

# Mecab-ko, mecab-ko-dic 설치
RUN apt-get install -y wget
WORKDIR /
RUN wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz
RUN wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz
RUN tar zxfv mecab-0.996-ko-0.9.2.tar.gz
RUN tar zxfv mecab-ko-dic-2.1.1-20180720.tar.gz
WORKDIR /mecab-0.996-ko-0.9.2
RUN ./configure && make && make check && make install
WORKDIR /mecab-ko-dic-2.1.1-20180720
RUN ldconfig && ./configure && make && make check && make install

# MeCab python binding
WORKDIR /
RUN apt-get install -y git
RUN git clone https://github.com/jonghwanhyeon/python-mecab-ko
WORKDIR /python-mecab-ko
RUN pip3 install -r requirements.txt && python3 setup.py build && python3 setup.py install

# 소스코드 복사 및 작업 디렉토리 변경
COPY . /app
WORKDIR /app

# 패키지
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]