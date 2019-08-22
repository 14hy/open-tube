from app import db
from models.video import Video
import re
from .utils import *
import cv2
import imageio as io
from pathlib import Path


def extract_tag_from_table(vid):
    """DB에서 특정 테이블의 모든 코멘트의 태그들을 뽑습니다.

    :param vid: youtube videoID

    :return: tags_dict
    {
        time(sec): {
            'reply': list<str> 댓글들,
            'gif_path': gif 파일의 경로
        }
    }
    """

    conn = db.session.connection()
    result = conn.execute(f'select * from {vid.lower()}')

    tags_dict = {}

    p = re.compile('^(\d{1,2}:\d{1,2} ){1,}')  # find play tags

    for each in result:
        comm = each[1]
        tags = p.match(comm)
        if tags is None:
            continue
        tags = tags.group()
        # e.g '11:09 11:17 12:20 12:31 13:20 14:00 15:27 16:00 '
        tags = tags.split()

        for tag in tags:
            m, s = map(int, tag.split(':'))
            tag_time = int(m * 60 + s)
            tags_dict[tag_time] = tags_dict.get(tag_time, {
                'reply': [],
                'gif_path': None
            })
            tags_dict[tag_time]['reply'].append(comm)

    conn.close()

    return tags_dict


def tag_to_gif(file_path, tags_dict, gif_path, vid, uid):
    """tag_dict로 부터 gif를 저장하고 경로를 저장

    :param file_path: file_path
    :param tags_dict: tag dictionary
    :param gif_path: place to save gifs
    :return: tag_dict addded file path
    """
    p = Path(gif_path) / str(uid)
    if not p.exists():
        p.mkdir()
    p = Path(f'{gif_path}/{uid}/{vid}')
    if not p.exists():
        p.mkdir()
    gif_path = f'{gif_path}/{uid}/{vid}'

    vc = cv2.VideoCapture(file_path)
    gif_duration = 180
    skip_fps = 4

    for time, _ in tags_dict.items():
        imgs = []
        target_time = time * vc.get(CV_CAP_PROP_FPS)
        vc.set(CV_CAP_PROP_POS_FRAMES, target_time // skip_fps)
        for _ in range(gif_duration // skip_fps):
            vc.set(CV_CAP_PROP_POS_FRAMES, vc.get(CV_CAP_PROP_POS_FRAMES) + skip_fps)
            _, img = vc.read(True)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (int(1280 * 0.4), int(720 * 0.4)))
            imgs.append(img)
        file_path = f'{gif_path}/{time}.gif'
        tags_dict[time]['gif_path'] = file_path
        with io.get_writer(file_path, mode='I', duration=0.1) as writer:
            for img in imgs:
                writer.append_data(img)

    v: Video = Video.query.filter_by(vid=vid, uid=uid).first()
    v.reply_gif = tags_dict
    v.status = 'complete'
    db.session.commit()

    vc.release()

    return tags_dict
