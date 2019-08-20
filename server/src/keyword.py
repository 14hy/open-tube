import re
from collections import OrderedDict, Iterable
# from mecab import MeCab
# from konlpy.tag import Okt

# mecab = MeCab()
# mecab = Okt()


def _prep_text(text, morphs=False):
    """텍스트 전처리
    1. 대문자 -> 소문자
    2. 쓸모없는 문자 빈칸 대체
    3. 한글, 영어 제외 제거
    4. 형태소 분석

    text: string.
    morphs: bool, morhphs?

    :return: string.
    """
    replace_by_space = re.compile('[/(){}\[\]\|@,;]')  # TODO 추가할 것
    remove_except = re.compile('[^0-9가-힣a-z ㄱ-ㅎ]')  # 영어, 한글, 숫자제외하고 제거
    # stop_words = set([])  # TODO 추가할 것

    text = text.lower()
    text = re.sub(replace_by_space, ' ', text)
    text = re.sub(remove_except, '', text)
    text = text.split()
    # if morphs:
    #     text = ' '.join(text)
    #     text = mecab.morphs(text)

    return ' '.join(text)


def get_cnt_words(replies: Iterable, prep_fn=_prep_text) -> dict:
    """
    단어 빈도를 세줍니다.
    replies: string iterator, 댓글들

    prep_fn: 전처리 함수

    :return: dict, {string: int}
    """

    assert isinstance(replies, Iterable)

    cnt_words = OrderedDict()

    for reply in replies:
        if not isinstance(reply, str):
            reply = reply[1]
        reply = prep_fn(reply)
        for word in reply.split():
            cnt_words[word] = cnt_words.get(word, 0) + 1

    cnt_words: dict = {word: cnt for word, cnt in sorted(cnt_words.items(), key=lambda x: x[1], reverse=True)}
    # 내림차순 정렬 및 api 주기 좋은 json 형태로
    return cnt_words
