import cv2 as cv
from time import time
import os
from CAMERA_IPS import CAMERA01, CAMERA02
from utils import ReadCamera

# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "video_codec;h265_cuvid"

if __name__ == "__main__":
    ReadCamera(CAMERA02)