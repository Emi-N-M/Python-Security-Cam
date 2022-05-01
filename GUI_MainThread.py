import time

import Timer_Event
from Events import Event_Listener
from Camera.Cam_Controller import start as startCamera
from Camera.Cam_Controller import frames_queue
from Camera.Cam_Controller import set_movement_det
from tkinter import *
import numpy as np
from PIL import ImageTk, Image
from Events.Event import post_event

application_ON = True
TE = Timer_Event

# Setup event listeners
Event_Listener.setup_cam_event_handelers()
Event_Listener.setup_timer_event_handelers()
Event_Listener.setup_alarm_event_handelers()


# Start background threads
def turnOnCamera():
    TE.start()
    startCamera()


# Shutdown application
def exit_program():
    global application_ON
    post_event("exit_app", data=None)
    application_ON = False
    root.destroy()


def activate_movement_det():
    global deactivate_movement_detector, activate_movement_detector
    set_movement_det(True)
    activate_movement_detector.pack_forget()
    deactivate_movement_detector.pack()


def deactivate_movement_det():
    global activate_movement_detector, deactivate_movement_detector
    post_event("stop_alarm", data=None)
    set_movement_det(False)
    deactivate_movement_detector.pack_forget()
    activate_movement_detector = Button(root, text="Activate Movement Detector", padx=50, command=activate_movement_det)
    activate_movement_detector.pack()


# GUI setup
root = Tk()
root.title("WatchDog")
root.geometry("1080x720")

# Canvas solution
canvas = Canvas(root, bg="black", width=640, height=480)
canvas.pack()
new_frame = PhotoImage()

start_Button = Button(root, text="Start Camera", padx=50, command=turnOnCamera)
start_Button.pack()

stop_Button = Button(root, text="Stop", padx=50, command=exit_program)
stop_Button.pack()

activate_movement_detector = Button(root, text="Activate Movement Detector", padx=50, command=activate_movement_det)
deactivate_movement_detector = Button(root, text="Deactivate Movement Detector", padx=50,
                                      command=deactivate_movement_det)

activate_movement_detector.pack()


def updateCanvas():
    # global canvas, frames_queue
    global new_frame
    if frames_queue.empty():
        return
    new_frame = frames_queue.get()
    new_frame = np.reshape(new_frame, (480, 640))
    new_frame = Image.fromarray(new_frame)
    new_frame = ImageTk.PhotoImage(new_frame)
    canvas.create_image(0, 0, anchor=NW, image=new_frame)


def video_stream(frame):
    global canvas
    frame = np.reshape(frame, (1280, 720))
    frame = Image.fromarray(frame)
    updateCanvas(frame)


def mainLoop():
    global root
    while application_ON:
        root.update()
        root.update_idletasks()
        updateCanvas()



mainLoop()
# root.mainloop()
