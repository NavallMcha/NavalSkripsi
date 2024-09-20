import torch
import numpy as np
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
print("[INFO] Success")
