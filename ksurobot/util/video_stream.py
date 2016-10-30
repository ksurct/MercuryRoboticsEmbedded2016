import subprocess
import atexit

VIDEO_STRING = "gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' !  x264enc pass=qual quantizer=2 tune=zerolatency ! rtph264pay ! udpsink host={} port={}"

class VideoHandler(object):
    def __init__(self):
        self.process_handle = None

    def open_video(self, host, port):
        if self.process_handle is None:
            self.process_handle = subprocess.run(VIDEO_STRING.format(host, port), shell=True)

    def close_video(self):
        if self.process_handle is not None:
            self.process_handle.terminate()
            self.process_handle.wait()
            self.process_handle = None


video_handler = VideoHandler()
atexit.register(video_handler.close_video)
