# Open-Tube for youtube streamers

## 아코디언을 활용한 AI (Tensorflow, R 등) 프로그래밍

### 개발 동기

```
최대의 동영상 재생 사이트 유튜브에 많은 관심이 쏠리고 있습니다.
그에 따라 다양한 통계 분석 플랫폼들이 등장하고 있으며 수요가 증가하고 있습니다.
그 이유는 유튜브의 수많은 데이터를 분석하기 힘들며, 가공되어 있지 않기 때문에 기획자나 마케터들이 활용할 수가 없기 때문입니다. 
새로운 AI관련(딥러닝, 머신러닝...) 기술을 활용한 플랫폼은 경쟁력이 있을 것이라 생각하였습니다.
```

### 개발 목표

```
1. 유튜브관련 직종 사람들이 활용할 수 있는 서비스를 개발합니다.
2. 유튜브관련 서비스를 개발하고자 하는 사람들에게 데이터를 제공합니다.
```

### 주요기능

```
1. 댓글 감성분석, 키워드 추출, 비속어 확인
	- 영상 선호도 파악, 관심을 보이는 키워드 확인 가능
2. 영상에서 얼굴 인식
	- 추후 초상권을 위한 얼굴 익명화, 인물찾기등에 활용 가능
```

### 구조

![image](https://user-images.githubusercontent.com/12870549/63571288-bf903a00-c5ba-11e9-83b3-b374e84a79cf.png)

### AI

1. `감성분석`은 RNN 중 Bidirectioanl LSTM 구조를 사용해 직접 학습하여 사용하였습니다. 데이터셋으로는 [NSMC](https://github.com/e9t/nsmc) 의 한국어 문장 데이터와 [Sentiment140](http://help.sentiment140.com/for-students) 의 영어 문장 데이터를 사용 하였습니다. 기존 [google-bert](https://github.com/google-research/bert)  언어 모델에 레이어를 추가하여 Fine-tuning 하려 하였으나, 주어진 클라우드 플랫폼에서 GPU 사용이 불가능하여 지나친 성능이슈가 존재하여 경량화하였습니다.
2. `영상 얼굴 인식 모델`은 [face-detection-mobilenet-ssd](https://github.com/bruceyang2012/Face-detection-with-mobilenet-ssd)를 사용하였습니다. 마찬가지로 GPU사용이 불가능함으로써 최대한 가벼운 모델을 찾아 배포하기 알맞은 바이너리 포맷으로 변환-[notebook](https://nbviewer.jupyter.org/github/rhodochrosite/my-snippets/blob/master/2019_08/py2%26keras%20to%20saved_model.ipynb)한 후, 사용하였습니다.
3. 인식한 얼굴을 구분하기 위한 `얼굴 유사도 모델`또한 바이너리 포맷으로 변환-[notebook](https://nbviewer.jupyter.org/github/rhodochrosite/my-snippets/blob/master/2019_08/tf1%20eager%26tf.keras%20to%20saved_model.ipynb)하여 사용하였습니다. 얼굴을 인식이후, cropping 하여 얼굴만 잘라낸 후, 영상내의 얼굴들을 구별하기 위해 사용합니다. 

### Web UI

![gif](./assets/GIF.gif)

## 테스트하기

```bash
# git clone 받기
git clone https://github.com/open-tube/open-tube.git

# client 폴더로 이동
cd client

# 모듈 다운로드
npm install

# webpack-dev-server 실행
npm run dev

# 이후, localhost:9000에서 테스트
```

## 배포하기

```bash
# Develop 버전 배포
npm run bundle

# Production 버전 배포
npm run production

## main-bundle.js 생성 후, 아코디언에서 별도 빌드 (경로: /mnt/ssd/server/web-server)
```

## Accordion

###  배포

1. Flask: API서버 배포
2. Nginx: Web site 배포 [(Demo URL)](https://open-tube.kro.kr)
3. Tensorflow-serving: 모델배포를 위해 활용

![image-20190823123339540](http://ww3.sinaimg.cn/large/006y8mN6gy1g69gg43ftrj30zv0lr7d8.jpg)



### 활용 기술

- Language - python, javascript

- server: [requirements.txt](https://github.com/open-tube/open-tube/blob/master/server/requirements.txt)

- client: [package.json](https://github.com/open-tube/open-tube/blob/master/client/package.json)

- Database - Postgres, Firebase



## DEMO

- [DEMO URL](https://open-tube.kro.kr/login)



## License

- License: GPLv3



## etc

- 다른 세부사항은 `WIKI` 및 `Projects` 패널 참조 : [WIKI](https://github.com/open-tube/open-tube/wiki)

-  모델 배포 가이드 [WIKI](https://github.com/open-tube/open-tube/wiki/%F0%9F%93%9D-%EB%AA%A8%EB%8D%B8-%EB%B0%B0%ED%8F%AC-%EA%B0%80%EC%9D%B4%EB%93%9C)

- 서버 배포 가이드 [WIKI](https://github.com/open-tube/open-tube/wiki/%F0%9F%93%9D-%EC%84%9C%EB%B2%84-%EB%B0%B0%ED%8F%AC-%EA%B0%80%EC%9D%B4%EB%93%9C)

