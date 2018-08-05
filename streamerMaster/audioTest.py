import pyaudio
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK, output_device_index=0)
print ("recording...")
frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print ("finished recording")
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

"""import pyaudio
import time
import numpy as np
from matplotlib import pyplot as plt
import scipy.signal as signal

CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()


device_count = p.get_default_input_device_info()
pfile = pyaudio.pa.__file__



fulldata = np.array([])
dry_data = np.array([])

def main():
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    input=True,
                    output_device_index=0,
                    stream_callback=callback)
    
    stream.start_stream()
    
    while stream.is_active():
        time.sleep(10)
        stream.stop_stream()
    stream.close()
    
    numpydata = np.hstack(fulldata)
    plt.plot(numpydata)
    plt.title("Wet")
    plt.show()
    
    
    numpydata = np.hstack(dry_data)
    plt.plot(numpydata)
    plt.title("Dry")
    plt.show()


    p.terminate()

def callback(in_data, frame_count, time_info, flag):
    global b,a,fulldata,dry_data,frames 
    audio_data = np.fromstring(in_data, dtype=np.float32)
    dry_data = np.append(dry_data,audio_data)
    #do processing here
    fulldata = np.append(fulldata,audio_data)
    return (audio_data, pyaudio.paContinue)

main()"""