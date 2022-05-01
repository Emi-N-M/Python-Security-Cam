import time
from Events.Event import post_event
import threading

timer_on = True
duration = 5



def throwEvent():
    print("Event posted")
    post_event("end_of_recording", True)


def timer():
    global timer_on, duration
    initial_time = time.perf_counter()
    final_time = initial_time + duration
    while timer_on:
        time.sleep(1)       #Sleep to improve performance
        if final_time < time.perf_counter():
            initial_time = time.perf_counter()
            final_time = initial_time + duration
            throwEvent()


def stop_timer(data):
    global timer_on
    timer_on = False


def start():
    timer_thread = threading.Thread(target=timer)
    timer_thread.start()

