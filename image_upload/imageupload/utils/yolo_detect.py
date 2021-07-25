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


def draw_bbox(boxes, scores, image ,image1):
    imH, imW, _ = image.shape
    count = 0
    for i in tqdm(range(len(scores[0]))):
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

            cv2.rectangle(image1, (xmin, ymin), (xmax, ymax), (10, 255, 0), bbox_thick)

            label = '%s: %d%%' % ("fish", int(score * 100))
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, fontScale,
                                                  bbox_thick)  # Get font size
            label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window

            cv2.rectangle(image1, (xmin, label_ymin - labelSize[1] - 5),
                          (xmin + labelSize[0], label_ymin + baseLine - 5), (255, 255, 255),
                          cv2.FILLED)  # Draw white box to put label text in
            cv2.putText(image1, label, (xmin, label_ymin - 2), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 0, 0),
                        bbox_thick)  # Draw label text
    return image1, count
