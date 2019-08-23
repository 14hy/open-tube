from models.download import Download
from models.video import Video
from src.download import download_url
import pytube
import cv2
import matplotlib.pyplot as plt
from app import db
from pathlib import Path
from .utils import *


def make_thumbnail(vid, uid, save_path, grid=(4, 1)):
    """썸네일 이미지를 생성하여 저장.

    :param vid: videoID
    :param save_path: string
    :param grid: tuple,

    :return: 성공여부
    """
    p = Path(save_path) / str(uid)
    if not p.exists():
        p.mkdir()
    p = Path(save_path) / str(uid) / str(vid)
    if not p.exists():
        p.mkdir()
    save_path = str(Path(f'{save_path}/{uid}/{vid}/{grid[0]}{grid[1]}.png'))
    try:
        d: Download = Download.query.filter_by(vid=vid).first()
    except:
        db.session.remove()
        db.session.rollback()
        d: Download = Download.query.filter_by(vid=vid).first()
    if d is None:
        download_url(vid, uid)
        try:
            v: Video = Video.query.filter_by(vid=vid, uid=uid).first()
        except:
            db.session.remove()
            db.session.rollback()
            v: Video = Video.query.filter_by(vid=vid, uid=uid).first()

        v.status = 'processing'
        db.session.commit()

        return {
            'status': 'wait'
        }
    file_path = d.file_path

    vc = cv2.VideoCapture(file_path)
    width = vc.get(CV_CAP_PROP_FRAME_WIDTH) * grid[1] * 0.01
    height = vc.get(CV_CAP_PROP_FRAME_HEIGHT) * grid[0] * 0.01

    _N = grid[0] * grid[1]

    fps = vc.get(CV_CAP_PROP_FRAME_COUNT) // _N - 1

    thumbnails = []

    # 썸네일 이미지 선택
    for i in range(_N):
        _, img = vc.read(True)  # -> tuple, [0]->status, [1]-> video, [height, width, channels]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #         img = cv2.resize(img, (512, 512))
        thumbnails.append(img)
        vc.set(CV_CAP_PROP_POS_FRAMES, vc.get(CV_CAP_PROP_POS_FRAMES) + fps)
    vc.release()

    # 썸네일 생성 및 저장
    fig = plt.figure(figsize=(width, height), dpi=100)
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
    axes = [fig.add_subplot(grid[0], grid[1], i, xticks=[], yticks=[]) for i in range(1, _N + 1)]
    for idx, axis in enumerate(axes):
        axis.imshow(thumbnails[idx])

    fig.tight_layout()
    plt.savefig(save_path, dpi=100, pad_inches=0)
    try:
        v: Video = Video.query.filter_by(vid=vid, uid=uid)
    except:
        db.session.remove()
        db.session.rollback()
        v: Video = Video.query.filter_by(vid=vid, uid=uid)
    v.thumbnails_path[f'{grid[0]}{grid[1]}'] = save_path
    db.session.commit()
