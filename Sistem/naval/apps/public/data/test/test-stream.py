# import libraries
from vidgear.gears import CamGear
import cv2

stream = CamGear(source='https://www.youtube.com/watch?v=Ww8hExYNQp0', stream_mode=True,
                 logging=True).start()  # YouTube Video URL as input

# infinite loop
while True:

    frame = stream.read()

    # check if frame is None
    if frame is None:
        # if True break the infinite loop
        break

    # do something with frame here
    frame = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Output Frame", frame)

    # Show output window
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
stream.stop()
