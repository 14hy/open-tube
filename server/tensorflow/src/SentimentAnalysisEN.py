from nltk.tokenize import word_tokenize
import pickle
import numpy as np
import pycurl
from io import BytesIO
import json
import pandas as pd


class SentimentAnalysisEN:
    def __init__(self, glove_path):
        with open(glove_path, "rb") as f:
            self.glove_dict = pickle.load(f)
        self.max_length = 250
        self.input_size = 200

    def embedding(self, word):
        if word in self.glove_dict.keys():
            return self.glove_dict[word]
        else:
            return np.random.normal(size=(self.input_size))

    def score(self, X):
        batch_size = len(X)

        c = pycurl.Curl()
        c.setopt(c.URL, "http://101.101.164.175:32357/v1/models/BiLSTM_EN:predict")
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])

        token_X = [word_tokenize(sentence) for sentence in X]
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


# 테스트
test = SentimentAnalysisEN(glove_path = "E:/jhm/open-tube/server/tensorflow/model/glove/glove.pickle")
X = [
    "hey fucking shit",
    "thanks"
]
test.score(X = X)