import threading
import pyaudio
import wave

# delcare alarm global variables
stream = None
wf = None
p = None


# initialize global vars
def set_global_vars():
    global wf, p, stream
    # alarm audio path here
    wf = wave.open('Media/Alarm_sound.wav', 'rb')
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream using callback
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)


# define callback
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)


def start_alarm():
    global stream
    set_global_vars()
    # start the stream
    stream.start_stream()

def stop_alarm():
    global stream
    if stream is not None:
        # stop stream
        stream.stop_stream()
        stream.close()
        wf.close()
        # close PyAudio
        p.terminate()


def start_alarm_thread():
    alarm_thread = threading.Thread(target=start_alarm)
    alarm_thread.start()
