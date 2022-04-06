from Event import subscribe
from Camera.Cam_Controller import setStopRecording, exit_cam



def handle_stopRecording_Event(data):
    setStopRecording(data)

def handle_turnOff_camera_Event(data):
    exit_cam()


def setup_cam_event_handelers():
    subscribe("end_of_recording", handle_stopRecording_Event)
    subscribe("exit_app", handle_turnOff_camera_Event)

