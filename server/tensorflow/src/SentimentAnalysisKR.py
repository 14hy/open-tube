from gensim.models import Word2Vec
import numpy as np
from konlpy.tag import Okt
import pycurl
from io import BytesIO
import json
import pandas as pd


class SentimentAnalysisKR:
    def __init__(self, word2vec_path):
        self.okt = Okt()
        self.word2vec = Word2Vec.load(word2vec_path)
        self.max_length = 100
        self.input_size = 300

    def embedding(self, word):
        if word in self.word2vec.wv.vocab:
            return self.word2vec.wv[word]
        else:
            return np.random.normal(size=(self.input_size))

    def score(self, X):
        batch_size = len(X)

        c = pycurl.Curl()
        c.setopt(c.URL, "http://101.101.164.175:32356/v1/models/BiLSTM_KR:predict")
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])

        token_X = [["/".join(tag) for tag in self.okt.pos(sentence, norm=True, stem=True)] for sentence in X]
        batch_X = [[self.embedding(word) for word in sentence] for sentence in token_X]
        batch_X_padded = np.zeros(shape=(batch_size, self.max_length, self.input_size))
        for b in range(batch_size):
            batch_X_padded[b, :len(batch_X[b])] = batch_X[b]
        seq_len_ = [len(x) for x in X]

        data = json.dumps({
            "inputs": {
                "input_X": batch_X_padded.tolist(),
                "dropout_keep_prob": 1.0,
                "seq_len": seq_len_
            }
        })

        buffer = BytesIO()

        c.setopt(c.POST, True)
        c.setopt(c.POSTFIELDS, data)
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()

        body = buffer.getvalue()
        pred = json.loads(body.decode('utf8'))["outputs"]
        pred = np.squeeze(pred)
        print(pred)

        df = pd.DataFrame(pred)
        return df

