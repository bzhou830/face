import cv2

class VideoCamera(object):
    def __init__(self):
        video_source = 'C:\\Users\\BineanZhou\\Desktop\\111.wmv'
        self.video = cv2.VideoCapture(video_source)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, image = self.video.read()
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()