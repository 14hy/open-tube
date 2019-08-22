import re

# @user_id => 제거
p_user = re.compile("@\S*\s")
# &amp; => &
p_amp = re.compile("&amp;")
# \\n => 공백
p_newline = re.compile("(\\n)+")
# xx:xx:xx => 제거후 저장
# 1:1이라는 것도 제거해버림 => 보완 필요
p_times = re.compile("\d+:\d+")
# emoji => <EMOJI>
# p_emoji = re.compile("[\U00010000-\U0010ffff]|[\u2000-\u2fff]", flags=re.UNICODE)
# http://~ => 제거
p_url = re.compile("https{0,1}://\S+\s")
# ㅋㅋ.. => ㅋㅋ
# ㅜㅜ.. ㅠㅠ.. => ㅠㅠ
# ㅎㅎ.. => ㅎㅎ
# .... ,,,, => ..
# !!.. => !
# ~~.. => ~
p_repeat1 = re.compile("ㅋㅋㅋ*")
p_repeat2 = re.compile("(ㅜㅜㅜ*)|(ㅠㅠㅠ*)")
p_repeat3 = re.compile("ㅎㅎㅎ*")
p_repeat4 = re.compile("(\.\.\.*)|(,,,*)")
p_repeat5 = re.compile("!!*")
p_repeat6 = re.compile("~~*")
p_repeat7 = re.compile("\?\?*")


times = []

def preprocess(sentences):
    sentences = list(sentences)
    for idx, row in enumerate(sentences):
        times_tmp = p_times.findall(row)
        if times_tmp != []:
            times.append(times_tmp)
        sentences[idx] = p_user.sub("", sentences[idx])
        sentences[idx] = p_amp.sub("&", sentences[idx])
        sentences[idx] = p_newline.sub(" ", sentences[idx])
        sentences[idx] = p_times.sub("", sentences[idx])
#         sentences[idx] = p_emoji.sub("<EMOJI>", sentences[idx])
        sentences[idx] = p_url.sub("", sentences[idx])
        sentences[idx] = p_repeat1.sub("ㅋㅋ", sentences[idx])
        sentences[idx] = p_repeat2.sub("ㅠㅠ", sentences[idx])
        sentences[idx] = p_repeat3.sub("ㅎㅎ", sentences[idx])
        sentences[idx] = p_repeat4.sub("..", sentences[idx])
        sentences[idx] = p_repeat5.sub("!", sentences[idx])
        sentences[idx] = p_repeat6.sub("~", sentences[idx])
        sentences[idx] = p_repeat7.sub("?", sentences[idx])
        sentences[idx] = sentences[idx].lower()
    return sentences, times