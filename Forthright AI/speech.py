import sounddevice as sd
import soundfile as sf

fs = 16000
recording = None

def start_recording():

    global recording

    print("Recording Started")

    recording = sd.rec(
        int(300 * fs),
        samplerate=fs,
        channels=1,
        dtype="float32"
    )

def stop_recording():

    global recording

    sd.stop()

    recording = recording * 2

    recording = recording.clip(-1, 1)

    sf.write(
        "audio/recording.wav",
        recording,
        fs
    )

    print("Recording Saved")

    return "audio/recording.wav"