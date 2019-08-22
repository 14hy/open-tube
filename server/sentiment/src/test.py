import sentiment_analysis

test_data = [
    "와...대박!",
    "미친놈인가???",
    "",
    "개꿀잼ㅋㅋㅋㅋㅋㅋㅋ",
    "베충인가?ㅉㅉ"
]

word2vec_path = "../model/word2vec/word2vec.model"
slang_dict_path = "../model/slang/slang_dict.txt"
sent = sentiment_analysis.SentimentAnalysis(word2vec_path, slang_dict_path)
index_list = [1,2,3,4,5]
print(sent.score(index_list, test_data))
print(sent.slang(index_list, test_data))
ban_list = [
    "베충"
]
print(sent.slang(index_list, test_data, ban_list))