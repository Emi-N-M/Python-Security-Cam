from .Event import subscribe
from Camera.Cam_Controller import setStopRecording, exit_cam
from Timer_Event import stop_timer
from Alarm import start_alarm_thread, stop_alarm


# Camera listener
def handle_stopRecording_Event(data):
    setStopRecording(data)


def handle_turnOff_camera_Event(data):
    exit_cam()


def setup_cam_event_handelers():
    subscribe("end_of_recording", handle_stopRecording_Event)
    subscribe("exit_app", handle_turnOff_camera_Event)


# Timer listener
def handle_stopTimer_Event(data):
    stop_timer(data)


def setup_timer_event_handelers():
    subscribe("exit_app", stop_timer)

# Alarm listener
def handle_movement_detected_Event(data):
    start_alarm_thread()

def handle_stop_alarm_Event(data):
    stop_alarm()

def setup_alarm_event_handelers():
    subscribe("movement_detected",handle_movement_detected_Event)
    subscribe("stop_alarm",handle_stop_alarm_Event)
    subscribe("exit_app",handle_stop_alarm_Event)
