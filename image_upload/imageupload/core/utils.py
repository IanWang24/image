import cv2
import numpy as np
import tensorflow as tf
from tqdm import tqdm


def process_data(frame):
    image_data = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_data = image_data / 255.
    images_data = []
    for i in range(1):
        images_data.append(image_data)
    images_data = np.asarray(images_data).astype(np.float32)
    batch_data = tf.constant(images_data)
    return batch_data


def draw_bbox(boxes, scores, image):
    imH, imW, _ = image.shape
    count = 0
    for i in range(len(scores[0])):
        if scores[0][i] > 0:
            count += 1
            # return!!!

            # init content
            fontScale = 0.4
            object_name = "fish"
            score = scores[0][i]
            box = boxes[0][i]

            ymin = int(box[0] * imH)
            ymax = int(box[2] * imH)
            xmin = int(box[1] * imW)
            xmax = int(box[3] * imW)

            bbox_thick = int(0.6 * (imH + imW) / 600)

            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), bbox_thick)

            label = '%s: %d%%' % ("fish", int(score * 100))
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, fontScale,
                                                  bbox_thick)  # Get font size
            label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window

            cv2.rectangle(image, (xmin, label_ymin - labelSize[1] - 5),
                          (xmin + labelSize[0], label_ymin + baseLine - 5), (255, 255, 255),
                          cv2.FILLED)  # Draw white box to put label text in
            cv2.putText(image, label, (xmin, label_ymin - 2), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 0, 0),
                        bbox_thick)  # Draw label text
    return image, count


def detect(img, ouput_path, model):
    # for Video
    # cap = cv2.VideoCapture(video_path)
    # cap.set(cv2.CAP_PROP_FPS, 30)  # set fps for my weak pc
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # out = cv2.VideoWriter(ouput_path, fourcc, 30, (416, 416))
    # if cap.isOpened():
    #     ret, frame = cap.read()
    #     print(frame)
    # else:
    #     print("error video path")

    
    
    batch_data = process_data(img)  # resize image and transform to tensor-like object

    # for using model to get predict information like: bondel boxes, scores or somthing

    pred_bbox = model(batch_data)
    for key, value in pred_bbox.items():
        boxes = value[:, :, 0:4]
        pred_conf = value[:, :, 4:]

    boxes, scores, _, _ = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=300,
        max_total_size=300,
        iou_threshold=0.45,
        score_threshold=0.70
    )

    img_tmp, c_tmp = draw_bbox(boxes, scores, img)  # draw bondel boxes and return counter

    
    cv2.imwrite('output.jpg', img_tmp)
    return c_tmp, img_tmp