import time
from Event import post_event, subscribe
import threading

timer_on = True

def throwEvent():
    print("Event posted")
    post_event("end_of_recording", True)


def timer():
    global timer_on
    while timer_on:
        time.sleep(5)   #Duration of the videos = 5sec /// Delays application shutdown!!!!
        throwEvent()

def stop_timer(data):
    global timer_on
    timer_on = False



def start():
    timer_thread = threading.Thread(target=timer)
    timer_thread.start()

def setup_timer_event_handelers():
    subscribe("exit_app", stop_timer)