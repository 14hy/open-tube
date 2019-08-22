## 감성 분석 word2vec 경로 설정

미리 학습된 word2vec 모델을 다운로드 [[구글 드라이브 경로]](https://drive.google.com/open?id=14oZHKc-omvqKdE3WDJzxYHOQDzvoXFWR)

```
word2vec.model
word2vec.model.trainables.syn1neg.npy
word2vec.model.wv.vectors.npy
```

파일을 한 폴더에 넣고 sentiment_analysis.py의 word2vec_path를 "~~/word2vec.model"로 설정