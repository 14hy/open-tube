import sentiment_analysis

test_data = [
    "와...대박!",
    "미친놈인가???",
    "개꿀잼ㅋㅋㅋㅋㅋㅋㅋ"
]

word2vec_path = "../model/word2vec/word2vec.model"
sent = sentiment_analysis.SentimentAnalysis(word2vec_path)
print(sent.score(test_data))