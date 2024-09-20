from onvif import ONVIFCamera
import cv2
import av
import numpy as np

# Konfigurasi kamera ONVIF
# camera_host = '192.168.137.180'  # Ganti dengan IP kamera ONVIF Anda
# camera_port = 8000               # Port kamera ONVIF 8000
# camera_user = 'admin'          # Username kamera ONVIF
# camera_pass = 'admin'      # Password kamera ONVIF

# # Inisialisasi koneksi kamera ONVIF
# camera = ONVIFCamera(camera_host, camera_port, camera_user, camera_pass)

# # Mendapatkan media service
# media_service = camera.create_media_service()

# # Mendapatkan profile media
# profiles = media_service.GetProfiles()
# profile = profiles[0]  # Menggunakan profile pertama

# # Mendapatkan stream URI
# stream_uri = media_service.GetStreamUri({
#     'StreamSetup': {
#         'Stream': 'RTP-Unicast',
#         'Transport': {
#             'Protocol': 'RTSP'
#         }
#     },
#     'ProfileToken': profile.token
# })

# print(stream_uri)
############################################################################
container = av.open("rtsp://admin:admin@192.168.137.107:8554/Streaming/Channels/101")
try:
    for frame in container.decode(video=0):
        frame = frame.to_ndarray(format='bgr24')
        frame = frame.astype(np.uint8)
        frame = cv2.resize(frame, (640, 480))
        cv2.imshow('ONVIF Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    container.close()
############################################################################


# rtsp_url = "rtsp://admin:admin@192.168.137.180:8554/Streaming/Channels/101"  # HD1  
# # rtsp_url = "rtsp://admin:admin@192.168.0.130:8554/Streaming/Channels/102" # SD
# print(f"RTSP URL: {rtsp_url}")
# container = av.open(rtsp_url)

# # Output file
# output_file = "output-video-16.mp4"
# output_container = av.open(output_file, mode='w')

# # Create a video stream for the output file
# stream = output_container.add_stream('h264', rate=30)
# stream.width = 640
# stream.height = 480
# stream.pix_fmt = 'yuv420p'

# try:
#     for frame in container.decode(video=0):
#         # Convert AV frame to OpenCV frame
#         frame = frame.to_ndarray(format='bgr24')
#         frame = cv2.resize(frame, (640, 480))
#         cv2.imshow('ONVIF Camera', frame)

#         # Convert back to AV frame and encode
#         new_frame = av.VideoFrame.from_ndarray(frame, format='bgr24')
#         for packet in stream.encode(new_frame):
#             output_container.mux(packet)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Flush the encoder
#     for packet in stream.encode():
#         output_container.mux(packet)
# finally:
#     cv2.destroyAllWindows()
#     container.close()
#     output_container.close()
