from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter
from modules.process import Procedure
import rospy

if __name__ == "__main__":
    try:
        rospy.init_node("cat_fur", anonymous=True)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            frame = cam.read(frame_size=480, show_fps=True)
            detect = rt.get(frame=frame)
            print(f"detect : {detect}")
            rt.draw(frame=frame, detection=detect)
            cam.show(frame, "frame")
            cam.wait(1)
    except rospy.ROSInterruptException:
        pass
