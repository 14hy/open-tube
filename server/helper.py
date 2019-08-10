## help function들을 모은 집합입니다
import subprocess

def __extract_save_reply(youtube_id):
    __cmd = f"youtube-comment-scraper --format csv -o {youtube_id}.csv {youtube_id}"
    try:
        subprocess.run(__cmd)
        return 1
    except Exception as e:
        print(e)
        return 0