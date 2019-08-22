import pytube
from app import db
from models.download import Download
import threading
import cv2
import numpy as np
import tensorflow as tf
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
        preds_decode = decode_y2(preds, 0.8, _IOU, img_height=720, img_width=1280, normalize_coords=True)

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
                        time_line[face_id].append({
                            time: preds_decode[idx_img][idx_face][2:].tolist()
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
                    time_line[unique_face_idx] = [{
                        time: preds_decode[idx_img][idx_face][2:].tolist()
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

def decode_y2(y_pred,
              confidence_thresh=0.5,
              iou_threshold=0.45,
              top_k='all',
              input_coords='centroids',
              normalize_coords=False,
              img_height=None,
              img_width=None):


    '''
    Convert model prediction output back to a format that contains only the positive box predictions
    (i.e. the same format that `enconde_y()` takes as input).

    Optionally performs confidence thresholding and greedy non-maximum suppression afte the decoding stage.

    Note that the decoding procedure used here is not the same as the procedure used in the original Caffe implementation.
    The procedure used here assigns every box its highest confidence as the class and then removes all boxes fro which
    the highest confidence is the background class. This results in less work for the subsequent non-maximum suppression,
    because the vast majority of the predictions will be filtered out just by the fact that their highest confidence is
    for the background class. It is much more efficient than the procedure of the original implementation, but the
    results may also differ.

    Arguments:
        y_pred (array): The prediction output of the SSD model, expected to be a Numpy array
            of shape `(batch_size, #boxes, #classes + 4 + 4 + 4)`, where `#boxes` is the total number of
            boxes predicted by the model per image and the last axis contains
            `[one-hot vector for the classes, 4 predicted coordinate offsets, 4 anchor box coordinates, 4 variances]`.
        confidence_thresh (float, optional): A float in [0,1), the minimum classification confidence in any positive
            class required for a given box to be considered a positive prediction. A lower value will result
            in better recall, while a higher value will result in better precision. Do not use this parameter with the
            goal to combat the inevitably many duplicates that an SSD will produce, the subsequent non-maximum suppression
            stage will take care of those. Defaults to 0.5.
        iou_threshold (float, optional): `None` or a float in [0,1]. If `None`, no non-maximum suppression will be
            performed. If not `None`, greedy NMS will be performed after the confidence thresholding stage, meaning
            all boxes with a Jaccard similarity of greater than `iou_threshold` with a locally maximal box will be removed
            from the set of predictions, where 'maximal' refers to the box score. Defaults to 0.45.
        top_k (int, optional): 'all' or an integer with number of highest scoring predictions to be kept for each batch item
            after the non-maximum suppression stage. Defaults to 'all', in which case all predictions left after the NMS stage
            will be kept.
        input_coords (str, optional): The box coordinate format that the model outputs. Can be either 'centroids'
            for the format `(cx, cy, w, h)` (box center coordinates, width, and height) or 'minmax'
            for the format `(xmin, xmax, ymin, ymax)`. Defaults to 'centroids'.
        normalize_coords (bool, optional): Set to `True` if the model outputs relative coordinates (i.e. coordinates in [0,1])
            and you wish to transform these relative coordinates back to absolute coordinates. If the model outputs
            relative coordinates, but you do not want to convert them back to absolute coordinates, set this to `False`.
            Do not set this to `True` if the model already outputs absolute coordinates, as that would result in incorrect
            coordinates. Requires `img_height` and `img_width` if set to `True`. Defaults to `False`.
        img_height (int, optional): The height of the input images. Only needed if `normalize_coords` is `True`.
        img_width (int, optional): The width of the input images. Only needed if `normalize_coords` is `True`.

    Returns:
        A python list of length `batch_size` where each list element represents the predicted boxes
        for one image and contains a Numpy array of shape `(boxes, 6)` where each row is a box prediction for
        a non-background class for the respective image in the format `[class_id, confidence, xmin, xmax, ymin, ymax]`.
    '''


    if normalize_coords and ((img_height is None) or (img_width is None)):
        raise ValueError("If relative box coordinates are supposed to be converted to absolute coordinates, the decoder needs the image size in order to decode the predictions, but `img_height == {}` and `img_width == {}`".format(img_height, img_width))

    # 1: Convert the classes from one-hot encoding to their class ID
    y_pred_converted = np.copy(y_pred[:,:,-14:-8]) # Slice out the four offset predictions plus two elements whereto we'll write the class IDs and confidences in the next step
    y_pred_converted[:,:,0] = np.argmax(y_pred[:,:,:-12], axis=-1) # The indices of the highest confidence values in the one-hot class vectors are the class ID
    y_pred_converted[:,:,1] = np.amax(y_pred[:,:,:-12], axis=-1) # Store the confidence values themselves, too

    # 2: Convert the box coordinates from the predicted anchor box offsets to predicted absolute coordinates
    if input_coords == 'centroids':
        y_pred_converted[:,:,[4,5]] = np.exp(y_pred_converted[:,:,[4,5]] * y_pred[:,:,[-2,-1]]) # exp(ln(w(pred)/w(anchor)) / w_variance * w_variance) == w(pred) / w(anchor), exp(ln(h(pred)/h(anchor)) / h_variance * h_variance) == h(pred) / h(anchor)
        y_pred_converted[:,:,[4,5]] *= y_pred[:,:,[-6,-5]] # (w(pred) / w(anchor)) * w(anchor) == w(pred), (h(pred) / h(anchor)) * h(anchor) == h(pred)
        y_pred_converted[:,:,[2,3]] *= y_pred[:,:,[-4,-3]] * y_pred[:,:,[-6,-5]] # (delta_cx(pred) / w(anchor) / cx_variance) * cx_variance * w(anchor) == delta_cx(pred), (delta_cy(pred) / h(anchor) / cy_variance) * cy_variance * h(anchor) == delta_cy(pred)
        y_pred_converted[:,:,[2,3]] += y_pred[:,:,[-8,-7]] # delta_cx(pred) + cx(anchor) == cx(pred), delta_cy(pred) + cy(anchor) == cy(pred)
        y_pred_converted = convert_coordinates(y_pred_converted, start_index=-4, conversion='centroids2minmax')
    elif input_coords == 'minmax':
        y_pred_converted[:,:,2:] *= y_pred[:,:,-4:] # delta(pred) / size(anchor) / variance * variance == delta(pred) / size(anchor) for all four coordinates, where 'size' refers to w or h, respectively
        y_pred_converted[:,:,[2,3]] *= np.expand_dims(y_pred[:,:,-7] - y_pred[:,:,-8], axis=-1) # delta_xmin(pred) / w(anchor) * w(anchor) == delta_xmin(pred), delta_xmax(pred) / w(anchor) * w(anchor) == delta_xmax(pred)
        y_pred_converted[:,:,[4,5]] *= np.expand_dims(y_pred[:,:,-5] - y_pred[:,:,-6], axis=-1) # delta_ymin(pred) / h(anchor) * h(anchor) == delta_ymin(pred), delta_ymax(pred) / h(anchor) * h(anchor) == delta_ymax(pred)
        y_pred_converted[:,:,2:] += y_pred[:,:,-8:-4] # delta(pred) + anchor == pred for all four coordinates
    else:
        raise ValueError("Unexpected value for `coords`. Supported values are 'minmax' and 'centroids'.")

    # 3: If the model predicts normalized box coordinates and they are supposed to be converted back to absolute coordinates, do that
    if normalize_coords:
        y_pred_converted[:,:,2:4] *= img_width # Convert xmin, xmax back to absolute coordinates
        y_pred_converted[:,:,4:] *= img_height # Convert ymin, ymax back to absolute coordinates

    # 4: Decode our huge `(batch, #boxes, 6)` tensor into a list of length `batch` where each list entry is an array containing only the positive predictions
    y_pred_decoded = []
    for batch_item in y_pred_converted: # For each image in the batch...
        boxes = batch_item[np.nonzero(batch_item[:,0])] # ...get all boxes that don't belong to the background class,...
        boxes = boxes[boxes[:,1] >= confidence_thresh] # ...then filter out those positive boxes for which the prediction confidence is too low and after that...
        if iou_threshold: # ...if an IoU threshold is set...
            boxes = _greedy_nms2(boxes, iou_threshold=iou_threshold, coords='minmax') # ...perform NMS on the remaining boxes.
        if top_k != 'all' and boxes.shape[0] > top_k: # If we have more than `top_k` results left at this point...
            top_k_indices = np.argpartition(boxes[:,1], kth=boxes.shape[0]-top_k, axis=0)[boxes.shape[0]-top_k:] # ...get the indices of the `top_k` highest-scoring boxes...
            boxes = boxes[top_k_indices] # ...and keep only those boxes...
        y_pred_decoded.append(boxes) # ...and now that we're done, append the array of final predictions for this batch item to the output list

    

    return y_pred_decoded

def _greedy_nms2(predictions, iou_threshold=0.45, coords='minmax'):	
    '''	
    The same greedy non-maximum suppression algorithm as above, but slightly modified for use as an internal	
    function in `decode_y2()`.	
    '''	
    boxes_left = np.copy(predictions)	
    maxima = [] # This is where we store the boxes that make it through the non-maximum suppression	
    while boxes_left.shape[0] > 0: # While there are still boxes left to compare...	
        maximum_index = np.argmax(boxes_left[:,1]) # ...get the index of the next box with the highest confidence...	
        maximum_box = np.copy(boxes_left[maximum_index]) # ...copy that box and...	
        maxima.append(maximum_box) # ...append it to `maxima` because we'll definitely keep it	
        boxes_left = np.delete(boxes_left, maximum_index, axis=0) # Now remove the maximum box from `boxes_left`	
        if boxes_left.shape[0] == 0: break # If there are no boxes left after this step, break. Otherwise...	
        similarities = iou(boxes_left[:,2:], maximum_box[2:], coords=coords) # ...compare (IoU) the other left over boxes to the maximum box...	
        boxes_left = boxes_left[similarities <= iou_threshold] # ...so that we can remove the ones that overlap too much with the maximum box	
    return np.array(maxima)


def convert_coordinates(tensor, start_index, conversion='minmax2centroids'):
    '''
    Convert coordinates for axis-aligned 2D boxes between two coordinate formats.
    Creates a copy of `tensor`, i.e. does not operate in place. Currently there are
    two supported coordinate formats that can be converted from and to each other:
        1) (xmin, xmax, ymin, ymax) - the 'minmax' format
        2) (cx, cy, w, h) - the 'centroids' format
    Note that converting from one of the supported formats to another and back is
    an identity operation up to possible rounding errors for integer tensors.
    Arguments:
        tensor (array): A Numpy nD array containing the four consecutive coordinates
            to be converted somewhere in the last axis.
        start_index (int): The index of the first coordinate in the last axis of `tensor`.
        conversion (str, optional): The conversion direction. Can be 'minmax2centroids'
            or 'centroids2minmax'. Defaults to 'minmax2centroids'.
    Returns:
        A Numpy nD array, a copy of the input tensor with the converted coordinates
        in place of the original coordinates and the unaltered elements of the original
        tensor elsewhere.
    '''
    ind = start_index
    tensor1 = np.copy(tensor).astype(np.float)
    if conversion == 'minmax2centroids':
        tensor1[..., ind] = (tensor[..., ind] + tensor[..., ind+1]) / 2.0 # Set cx
        tensor1[..., ind+1] = (tensor[..., ind+2] + tensor[..., ind+3]) / 2.0 # Set cy
        tensor1[..., ind+2] = tensor[..., ind+1] - tensor[..., ind] # Set w
        tensor1[..., ind+3] = tensor[..., ind+3] - tensor[..., ind+2] # Set h
    elif conversion == 'centroids2minmax':
        tensor1[..., ind] = tensor[..., ind] - tensor[..., ind+2] / 2.0 # Set xmin
        tensor1[..., ind+1] = tensor[..., ind] + tensor[..., ind+2] / 2.0 # Set xmax
        tensor1[..., ind+2] = tensor[..., ind+1] - tensor[..., ind+3] / 2.0 # Set ymin
        tensor1[..., ind+3] = tensor[..., ind+1] + tensor[..., ind+3] / 2.0 # Set ymax
    else:
        raise ValueError("Unexpected conversion value. Supported values are 'minmax2centroids' and 'centroids2minmax'.")

    return tensor1

def iou(boxes1, boxes2, coords='centroids'):
    '''
    Compute the intersection-over-union similarity (also known as Jaccard similarity)
    of two axis-aligned 2D rectangular boxes or of multiple axis-aligned 2D rectangular
    boxes contained in two arrays with broadcast-compatible shapes.
    Three common use cases would be to compute the similarities for 1 vs. 1, 1 vs. `n`,
    or `n` vs. `n` boxes. The two arguments are symmetric.
    Arguments:
        boxes1 (array): Either a 1D Numpy array of shape `(4, )` containing the coordinates for one box in the
            format specified by `coords` or a 2D Numpy array of shape `(n, 4)` containing the coordinates for `n` boxes.
            Shape must be broadcast-compatible to `boxes2`.
        boxes2 (array): Either a 1D Numpy array of shape `(4, )` containing the coordinates for one box in the
            format specified by `coords` or a 2D Numpy array of shape `(n, 4)` containing the coordinates for `n` boxes.
            Shape must be broadcast-compatible to `boxes1`.
        coords (str, optional): The coordinate format in the input arrays. Can be either 'centroids' for the format
            `(cx, cy, w, h)` or 'minmax' for the format `(xmin, xmax, ymin, ymax)`. Defaults to 'centroids'.
    Returns:
        A 1D Numpy array of dtype float containing values in [0,1], the Jaccard similarity of the boxes in `boxes1` and `boxes2`.
        0 means there is no overlap between two given boxes, 1 means their coordinates are identical.
    '''

    if len(boxes1.shape) > 2: raise ValueError("boxes1 must have rank either 1 or 2, but has rank {}.".format(len(boxes1.shape)))
    if len(boxes2.shape) > 2: raise ValueError("boxes2 must have rank either 1 or 2, but has rank {}.".format(len(boxes2.shape)))

    if len(boxes1.shape) == 1: boxes1 = np.expand_dims(boxes1, axis=0)
    if len(boxes2.shape) == 1: boxes2 = np.expand_dims(boxes2, axis=0)

    if not (boxes1.shape[1] == boxes2.shape[1] == 4): raise ValueError("It must be boxes1.shape[1] == boxes2.shape[1] == 4, but it is boxes1.shape[1] == {}, boxes2.shape[1] == {}.".format(boxes1.shape[1], boxes2.shape[1]))

    if coords == 'centroids':
        # TODO: Implement a version that uses fewer computation steps (that doesn't need conversion)
        boxes1 = convert_coordinates(boxes1, start_index=0, conversion='centroids2minmax')
        boxes2 = convert_coordinates(boxes2, start_index=0, conversion='centroids2minmax')
    elif coords != 'minmax':
        raise ValueError("Unexpected value for `coords`. Supported values are 'minmax' and 'centroids'.")

    intersection = np.maximum(0, np.minimum(boxes1[:,1], boxes2[:,1]) - np.maximum(boxes1[:,0], boxes2[:,0])) * np.maximum(0, np.minimum(boxes1[:,3], boxes2[:,3]) - np.maximum(boxes1[:,2], boxes2[:,2]))
    union = (boxes1[:,1] - boxes1[:,0]) * (boxes1[:,3] - boxes1[:,2]) + (boxes2[:,1] - boxes2[:,0]) * (boxes2[:,3] - boxes2[:,2]) - intersection

    return intersection / union

if __name__ == '__main__':
    # download_url('https://www.youtube.com/watch?v=Vp3fWnf1DoM')
    pass
