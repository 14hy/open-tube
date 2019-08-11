## help function들을 모은 집합입니다
import subprocess

def extract_save_reply(youtube_id):
    __cmd = f"youtube-comment-scraper --format csv -o ./csv/{youtube_id}.csv {youtube_id}"
    try:
        subprocess.call(__cmd, shell=True)
        return 1
    except Exception as e:
        print(e)
        return 0
