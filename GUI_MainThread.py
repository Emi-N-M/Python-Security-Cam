import Timer_Event
from Camera import Cam_Listener
from Camera.Cam_Controller import start as startCamera
from Camera.Cam_Controller import frames_queue
from tkinter import *
import numpy as np
from PIL import ImageTk, Image
from Event import subscribe, post_event

TE = Timer_Event
Cam_Listener.setup_cam_event_handelers()
Timer_Event.setup_timer_event_handelers()

root = Tk()
root.title("WatchDog")
root.geometry("1280x720")

# Canvas solution
canvas = Canvas(root, bg="black", width=640, height=480)
canvas.pack()
new_frame = PhotoImage()


# Start background threads
def turnOnCamera():
    TE.start()
    startCamera()


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


def exit_program():
    post_event("exit_app", data=None)
    root.destroy()


start_Button = Button(root, text="Start Camera", padx=50, command=turnOnCamera)
start_Button.pack()

stop_Button = Button(root, text="Stop", padx=50, command=exit_program)
stop_Button.pack()


def mainLoop():
    while True:
        root.update()
        root.update_idletasks()
        updateCanvas()


mainLoop()
# root.mainloop()
