import pytube
from app import db
from models.download import Download
import threading
import cv2
import numpy as np
import tensorflow as tf
from ssd_box_encode_decode_utils import decode_y2
from pathlib import Path
import json
from multiprocessing import Process

print(f'tensorflow - {tf.__version__}')

CV_CAP_PROP_POS_MSEC = 0  # Current position of the video file in milliseconds or video capture timestamp.
CV_CAP_PROP_POS_FRAMES = 1  # 0-based index of the frame to be decoded/captured next.
CV_CAP_PROP_FRAME_WIDTH = 3  # Width of the frames in the video stream.
CV_CAP_PROP_FRAME_HEIGHT = 4  # Height of the frames in the video stream.
CV_CAP_PROP_FPS = 5  # Frame rate.
CV_CAP_PROP_FRAME_COUNT = 7  # Number of frames in the video file.

_CONF = 0.01
_IOU = 0.15
processes = []
ssd_path = '/mnt/master/models/ssd-face/0001'
# ssd_path = '/Users/minhyeoklee/PycharmProjects/open-tube/server/ssd-face/0001'
similarity_path = '/mnt/master/models/face-similarity/1'
# similarity_path = '/Users/minhyeoklee/PycharmProjects/open-tube/server/face-similarity/1'
face_dir = '/mnt/master/faces'

model_ssd = tf.saved_model.load(ssd_path)
model_sim = tf.saved_model.load(similarity_path)

infer_similarity = model_sim.signatures['serving_default']
infer_ssd = model_ssd.signatures['serving_default']


def _get_anoymous_features(vid):
    """영상을 열고, 영상에서 얼굴을 인식하고 유사도를 비교한 뒤
    프론트에서 사용할 타임라인데이터를 만들어 전달합니다.

    :return: time line dict
    {
        faceid: [integer seconds...]
    }
    """
    # base_dir = os.environ['FACES_BASE_DIR']
    _fps_per_sec = 1.0
    _batch_size = 5
    _DIST_THRESHOLD = 0.5
    unique_face_idx = 0
    FACES = {}
    time_line = {}
    time = 0

    q = Download.query.filter_by(vid=vid).first()
    uid = q.uid
    file_path = q.file_path

    vc = cv2.VideoCapture(file_path)

    dataset = tf.data.Dataset.from_generator(_input_fn(vc, _fps_per_sec), output_types='float32').batch(_batch_size)
    print('start making time line data...')
    print(f'uid: {uid}')
    print(f'file_path: {file_path}')
    for idx_dataset, imgs in enumerate(dataset):
        preds = infer_ssd(imgs)['predicts'].numpy()
        preds_decode = decode_y2(preds, 0.8, img_height=512, img_width=512, normalize_coords=True)

        for idx_img, img in enumerate(imgs.numpy()):
            time += 1
            faces = _croped_faces(img, preds_decode[idx_img], resize=True)
            if not faces:
                continue

            faces = np.array(faces)
            preds_similarity = infer_similarity(norm_imgs(faces))['output_1']

            for idx_face, pred_similarity in enumerate(preds_similarity):
                # 예측한 얼굴들의 피쳐벡터와 기존에 등록된 얼굴들을 비교하고, 없으면 추가. 있으면 시간초만 추가.
                found = False
                # False --> 새로운 얼굴 발견
                for face_id, feature in FACES.items():
                    dist = l1_distance(feature, pred_similarity.numpy())
                    if dist < _DIST_THRESHOLD:
                        xmin, xmax, ymin, ymax = preds_decode[idx_img][idx_face][2:].tolist()
                        width = abs(xmax - xmin)
                        height = abs(ymax - ymin)

                        time_line[face_id].append({
                            time: [xmin * 1280, ymax * 720, width * 1280, height * 720]
                        })
                        found = True
                if not found:
                    # 새로운 얼굴추가
                    path = Path(f'{face_dir}/{uid}/{vid}')
                    if not Path(f'{face_dir}/{uid}').exists():
                        Path(f'{face_dir}/{uid}').mkdir()
                    if not path.exists():
                        print(f'making new directory in {str(path)}..')
                        path.mkdir()
                    cv2.imwrite(f'{face_dir}/{uid}/{vid}/{unique_face_idx}.jpg',
                                cv2.cvtColor(faces[idx_face], cv2.COLOR_RGB2BGR))
                    FACES[unique_face_idx] = pred_similarity.numpy()

                    xmin, xmax, ymin, ymax = preds_decode[idx_img][idx_face][2:].tolist()
                    width = abs(xmax - xmin)
                    height = abs(ymax - ymin)

                    time_line[unique_face_idx] = [{
                        time: [xmin * 1280, ymax * 720, width * 1280, height * 720]
                    }]
                    unique_face_idx += 1

    # 분석종료
    q.status = 'completed'
    db.session.commit()

    return time_line


def norm_imgs(imgs):
    imgs = imgs - 127.5
    imgs = imgs / 127.5
    imgs = imgs.astype('float32')
    return tf.convert_to_tensor(imgs)


def _download(vid, stream=None):
    """영상을 다운로드 받은 후, 익명화를 위한 데이터를 만듭니다.
    :param vid:
    :param stream:
    :return:
    """

    try:
        if stream is not None:
            file_path = stream.download(output_path=f'{face_dir}/../downloads')
            print('download done')
    except:
        file_path = None
        print('download failed')
    finally:
        d = Download.query.filter_by(vid=vid).first()
        if not file_path and stream is not None:
            d.status = 'failed'
            db.session.commit()
        elif stream is not None:
            d.file_path = file_path
            d.status = 'downloaded'
            db.session.commit()

    if d.status == 'downloaded':
        d.status = 'processing'
        db.session.commit()
        time_line = _get_anoymous_features(vid)
        d = Download.query.filter_by(vid=vid).first()
        d.time_line = json.dumps(time_line)
        db.session.commit()


def download_url(vid, uid, res='720p', fps=30):
    """영상을 다운로드 하고 저장된 상태를 리턴
    """
    q = Download.query.filter_by(vid=vid, uid=uid).first()
    if q is not None:
        if q.status == 'processing':
            return {
                'status': q.status
            }
        if q.status == 'downloading':
            return {
                'status': 'wait'
            }
        if q.status == 'downloaded':
            _download(vid)
            return {
                'status': 'processing'
            }
        if q.status == 'completed':
            return {
                'status': 'complete',
                'time_line': q.time_line
            }
    else:

        d = Download(vid=vid, status='downloading', uid=uid)
        db.session.add(d)
        db.session.commit()

        base_url = 'https://www.youtube.com/watch?v='
        url = base_url + vid

        print(f'download start url: {url} from user {uid}')
        yt = pytube.YouTube(url)
        streams = yt.streams.all()
        stream = None
        for each in streams:
            if each.fps == fps and each.resolution == res:
                stream = each
                break
        processes.append(Process(target=_download, kwargs={'vid': vid, 'stream': stream}))
        processes[-1].start()
        return {
            'status': 'wait'
        }


def _croped_faces(img, results, resize=False):
    """얼굴을 cropping하여 추출
    img: ndarray, 원본이미지 하나
    results: 얼굴인식 예측값, (None, 6)
    [0] -> 라벨
    [1] - > confidence
    [2] ~[5] -> xmin, xmax, ymin, ymax

    :return: faces list
    """
    _IMG_SIZE = 50
    _CONF = 0.9

    img = np.array(img)

    faces = []
    for each in results:
        #             print(each[1])
        if each[1] < _CONF:
            continue

        xmin, xmax = int(each[2]), int(each[3])
        ymin, ymax = int(each[4]), int(each[5])
        if xmin < 0 or xmax < 0 or ymin < 0 or ymax < 0:  # 가끔 마이너스가 옴.
            continue

        if xmax - xmin <= _IMG_SIZE and ymax - ymin <= _IMG_SIZE:
            continue

        face = img[ymin:ymax, xmin:xmax].copy().astype('uint8')
        #         plt.imshow(face)
        #         plt.show()
        if resize:
            face = cv2.resize(face, (128, 128))
        faces.append(face)
    return faces


def l1_distance(a, b):
    if a is None or b is None:
        return 99.9

    a = np.array(a)
    b = np.array(b)

    l1 = a - b
    l1 = np.square(l1)
    l1 = np.sum(l1)
    l1 = np.sqrt(l1 + 1e-8)
    return l1


def _input_fn(vc, per_sec):
    def img_generator():
        fps = round(vc.get(CV_CAP_PROP_FPS)) // per_sec

        while True:
            #             print(vc.get(CV_CAP_PROP_POS_FRAMES))
            status, img = vc.read()

            if not status:
                raise StopIteration

            img = cv2.resize(img, (512, 512))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #             img = pickle.dumps(img)
            #             img = img.tolist()
            img = img.astype('float32')

            yield img

            vc.set(CV_CAP_PROP_POS_FRAMES, vc.get(CV_CAP_PROP_POS_FRAMES) - 1 + fps)

    return img_generator


if __name__ == '__main__':
    # download_url('https://www.youtube.com/watch?v=Vp3fWnf1DoM')
    pass
