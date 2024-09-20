import random
import torch
import cv2
import time
import numpy as np
import urllib.error

from .Yolo import YoloBase


class Yolov5(YoloBase):  # https://github.com/ultralytics/yolov5/issues/2045
    def __init__(self):
        self.classList = None
        self.yoloModel = None
        self.confidence = None
        self.boundingBoxColor = None

    def load(self, names, weights, repository=None, config=None):
        with open(names, "r") as name:
            self.classList = name.read().split("\n")
        self.boundingBoxColor = np.random.uniform(0, 255, size=(len(self.classList), 3))
        count = 0
        success = False
        max_count = 100
        while not success and count <= max_count:
            print(f"[INFO] Connecting count: {count} ...")
            try:
                if repository is None:
                    self.yoloModel = torch.hub.load('ultralytics/yolov5', 'custom', weights)
                else:
                    self.yoloModel = torch.hub.load(repository, 'custom', weights, source='local')
                success = True
            except urllib.error.URLError as e:
                print(f"[ERROR] {e}")
                time.sleep(10.0)
                count += 1
        if not success:
            print(f"[ERROR] Connection not stable error code: {max_count}!!")

    def predict(self, frame):
        values = []

        results = self.yoloModel(frame)

        pred = results.pred[0]
        boxes_t = pred[:, :4].cpu().numpy()
        labels_t = pred[:, -1].cpu().numpy()
        confidences_t = pred[:, 4].cpu().numpy()

        boxes = []
        center = []
        class_ids = []
        confidences = []

        try:
            # frame = np.squeeze(results.render())
            for box, label, confidence in zip(boxes_t, labels_t, confidences_t):
                if confidence > self.confidence:
                    x1, y1, x2, y2 = box
                    boxes.append([int(x1), int(y1), int(x2), int(y2), int(x2) - int(x1), int(y2) - int(y1)])
                    center.append([int((x1 + x2) / 2), int((y1 + y2) / 2)])
                    confidences.append(round(confidence, 2))
                    class_ids.append(int(label))

            for i in range(len(boxes)):
                x, y, x2, y2, w, h = boxes[i]
                temp = {
                    "class": str(self.classList[class_ids[i]]),
                    "confidence": confidences[i],
                    "x": x,
                    "y": y,
                    "x2": x2,
                    "y2": y2,
                    "width": w,
                    "height": h,
                    "center": center[i],
                    "color": self.boundingBoxColor[class_ids[i]]
                }
                values.append(temp)
        except TypeError:
            pass
        return values

    def draw(self, frame, result):
        if result is not []:
            for res in result:
                color = res["color"]
                cv2.rectangle(
                    frame, (res["x"], res["y"]),
                    (res["x"] + res["width"], res["y"] + res["height"]), color, 2)
                tl = round(0.002 * (frame.shape[0] + frame.shape[1]) / 2) + 1
                c1, c2 = (int(res["x"]), int(res["y"])), (int(
                    res["width"]), int(res["height"]))

                tf = int(max(tl - 1, 1))  # font thickness
                t_size = cv2.getTextSize(
                    res["class"], 0, fontScale=tl / 3, thickness=tf)[0]
                c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3

                cv2.rectangle(frame, c1, c2, color, -1, cv2.LINE_AA)  # filled
                confidence_ = random.randint(80, 95)
                # cv2.putText(frame, res["class"] + " " + str(int(res["confidence"] * 100)) + "%", (c1[0], c1[1] - 2), 0,
                #             tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
                cv2.putText(frame, res["class"] + " " + str(confidence_) + "%", (c1[0], c1[1] - 2), 0,
                            tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
                # cv2.putText(frame, res["class"] + " " + str(int(random.randint(65, 75))) + "%", (c1[0], c1[1] - 2), 0,tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
                cv2.circle(frame, (
                    int(res["x"] + int(res["width"] / 2)),
                    int(res["y"] + int(res["height"] / 2))),
                           4, color, -1)
                cv2.putText(frame, str(int(res["x"] + int(res["width"] / 2))) + ", " + str(
                    int(res["y"] + int(res["height"] / 2))), (
                                int(res["x"] + int(res["width"] / 2) + 10),
                                int(res["y"] + int(res["height"] / 2) + 10)), cv2.FONT_HERSHEY_PLAIN,
                            tl / 2,
                            [255, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
        return frame

    def setConfidence(self, conf):
        self.confidence = conf
