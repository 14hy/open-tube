from gensim.models import Word2Vec
import numpy as np
from konlpy.tag import Okt
import pycurl
import pandas as pd
from io import BytesIO
import json
import sentiment.src.preprocess


class SentimentAnalysis:
    def __init__(self, word2vec_path):
        self.okt = Okt()
        self.word2vec = Word2Vec.load(word2vec_path)
        self.max_length = 250
        self.input_size = 256

    def embedding(self, word):
        return self.word2vec.wv[word]

    def tokenize(self, data):
        tokens = []
        for sentence in data:
            tags = self.okt.pos(sentence, norm=True, stem=True)
            tmp = []
            for tag in tags:
                if tag[1] == "Foreign":
                    tag = ("<EMOJI>", "Foreign")
                tag = "/".join(tag)
                if tag not in self.word2vec.wv.vocab:
                    tag = "<UNK>"
                tmp.append(tag)
            tokens.append(tmp)
        return tokens

    def score(self, X):
        batch_size = len(X)

        c = pycurl.Curl()
        c.setopt(c.URL, "http://101.101.167.71:32359/v1/models/sentiment-analysis:predict")
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])

        X, _ = preprocess.preprocess(X)
        token_X = self.tokenize(X)

        for idx, token in enumerate(token_X):
            if len(token) == 0:
                token_X[idx] = ["<UNK>"]
            elif len(token) > self.max_length:
                token_X[idx] = token[:self.max_length]

        batch_X = [[self.embedding(word) for word in sentence] for sentence in token_X]
        batch_X_padded = np.zeros(shape=(batch_size, self.max_length, self.input_size))
        for b in range(batch_size):
            batch_X_padded[b, :len(batch_X[b])] = batch_X[b]
        seq_len_ = [len(x) for x in batch_X]

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

