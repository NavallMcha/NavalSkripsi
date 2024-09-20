import cv2
import numpy as np
from abc import ABC, abstractmethod


class YoloBase(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load(self, names, weights, config=None):
        pass

    @abstractmethod
    def predict(self, frame):
        pass

    @abstractmethod
    def draw(self, frame, result):
        pass

    @abstractmethod
    def setConfidence(self, conf):
        pass

    @staticmethod
    def filterByClass(listResult, *classNames):
        return [item for item in listResult if item['class'] in list(classNames)]

    @staticmethod
    def countByClass(listResult, className):
        return len([item for item in listResult if item['class'] == className])

    @staticmethod
    def getAreaByClass(listResult):
        areas = []
        for res in listResult:
            x, y, width, height = res['x'], res['y'], res['width'], res['height']
            temp = [[x, y], [x + width, y], [x + width, y + height], [x, y + height]]
            areas.append(temp)
        return areas

    @staticmethod
    def drawArea(frame, area):
        cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 255, 0), 2)

    @staticmethod
    def isInArea(result, area):
        res = cv2.pointPolygonTest(np.array(area, np.int32), (result["x"], result["y"]), False)
        return res >= 0

    @staticmethod
    def isAreaOverlapping(res1, res2, option=False):
        r1x1, r1y1, r1x2, r1y2 = res1['x'], res1['y'], res1['x2'], res1['y2']
        r2x1, r2y1, r2x2, r2y2 = res2['x'], res2['y'], res2['x2'], res2['y2']

        if option:
            return r1x1 > r2x1 and r1y1 > r2y1 and r1x2 < r2x2 and r1y2 < r2y2
        else:
            r1w, r1h = res1['width'], res1['height']
            r2w, r2h = res2['width'], res2['height']
            return not (r1x1 > r2x1 + r2w or r1x1 + r1w < r2x1 or r1y1 > r2y1 + r2h or r1y1 + r1h < r2y1)

    @staticmethod
    def getROI(frame, result):
        return frame[result["y"]:result["y"] + result["height"], result["x"]:result["x"] + result["width"]]

    @staticmethod
    def getXYXYArray(listResult):
        return np.asarray([[res["x"], res["y"], res["x2"], res["y2"], res["confidence"]] for res in listResult])

    @staticmethod
    def getXYXY(result):
        return result["x"], result["y"], result["x2"], result["y2"], result["confidence"]
