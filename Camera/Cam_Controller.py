import os
import threading
import queue
import cv2
import subprocess
import numpy as np
from Events.Event import post_event

stopRecording = False
camera_on = True
movement_detector_ON = False
frames_queue = queue.Queue()


def start():
    cam_thread = threading.Thread(target=mainLoop)
    cam_thread.start()


def mainLoop():
    global camera_on
    while camera_on:
        recordVideo()


def setStopRecording(data):
    global stopRecording
    stopRecording = data


def exit_cam():
    global camera_on, stopRecording
    stopRecording = True
    camera_on = False
    print("EXIT CAM CAMERA_ON: ", camera_on)

def set_movement_det(data):
    global movement_detector_ON
    movement_detector_ON = data

# Write video in to a file.avi
def recordVideo():
    print("CAMERA_ON: ", camera_on)
    path = "/home/emilio/VIDEOS/"
    filename = path + setVideoFileName(path)
    frames_per_second = 20.0
    resolution = '480p'
    cap = cv2.VideoCapture(0)
    dims = get_dims(cap, resolution)
    video_type_cv2 = get_video_type(filename)
    global stopRecording, frames_queue, movement_detector_ON
    stopRecording = False
    print("PATH: " + filename)
    out = cv2.VideoWriter(filename, video_type_cv2, frames_per_second, dims)
    frame_cont = 0

    while True:
        print("Cam While")
        # Display Video
        ret, frame = cap.read()
        # Convert frame into GRAY-scale to work with PIL library
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames_queue.put(gray)

        # Movement detector code
        if movement_detector_ON:
            frame_cont += 1
            noise_tolerance = 15
            if frame_cont == 1:
                first_frame = frame
            else:
                second_frame = first_frame
                first_frame = frame
                diff = cv2.absdiff(first_frame, second_frame)
                gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # gray??

                # If the value of any pixel in gray_diff is noise_tolerance or lower, then set it to zero
                gray_diff[gray_diff <= noise_tolerance] = 0
                gray_diff_value_mean = np.mean(gray_diff)
                movement = gray_diff_value_mean > 1     # Min value of gray_diff_value_mean to detect movement = 1 (?)
                if movement:
                    post_event("movement_detected",data=None)
                    movement_detector_ON = False

                print("Movement?: ", movement )

        # Write Video
        out.write(frame)
        if stopRecording:  # Mark to cut the current video
            break

    cap.release()
    out.release()
    # cv2.destroyAllWindows()

    # Make the output video lighter              ------ INSTALL ffmpeg IN CPU ---------
    # bashCommand = "ffmpeg -i video.avi video_light.avi"
    # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    # stdout, stderr = process.communicate()

    # os.system(bashCommand)


def get_video_type(filename):
    VIDEO_TYPE = {
        'avi': cv2.VideoWriter_fourcc('M', 'P', 'E', 'G'),
        # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }

    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


def setVideoFileName(path):
    defaultName = 'video.avi'
    versionNumber = 1
    bashCommand = "ls " + path
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    file = stdout.decode('utf-8')

    while True:
        if defaultName not in file:
            break
        defaultName = ''.join([i for i in defaultName if not i.isdigit()])
        defaultName = defaultName.split('.')[0] + str(versionNumber) + ".avi"
        versionNumber += 1
    return defaultName


def get_dims(cap, res):
    STD_DIMENSIONS = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080)
    }
    width, height = STD_DIMENSIONS['480p']
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    change_res(cap, width, height)
    return width, height
