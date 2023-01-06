import pyaudio
import numpy as np
import time
from scipy import signal
import matplotlib.pyplot as plt
from pprint import pprint

x = np.linspace(0, np.pi*4, 600)
y = np.sin(x)
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(28,25))
ax.set_ylim(-7,7)
ax.plot(x,y,lw=5, c="white", alpha=1)

p = pyaudio.PyAudio()
CHANNELS = 1
RATE = 44100
CHUNK=200
def callback(in_data, frame_count, time_info, flag):
    audio_data = np.fromstring(in_data, dtype=np.float32)
    pprint(audio_data.shape[0]);
    x = np.linspace(0, np.pi*2, audio_data.shape[0])
    fundamental = np.sin(x*5)
    #hamonic1 = np.sin(x*440)
    #hamonic2 = np.sin(x*880)
    #audio_data = (fundamental + hamonic1 + hamonic2)
    #audio_data += fundamental
    #audio_data += fundamental

    ##return in_data, pyaudio.paContinue
    return audio_data.astype(np.float32), pyaudio.paContinue

grabando = True
stream = p.open(
    format=pyaudio.paInt16,
    channels=CHANNELS,
    frames_per_buffer=CHUNK,
    rate=RATE,
    output = True,
    input = True,
    stream_callback=callback
)
stream.start_stream()
while grabando==True:
    print("Escuchooo")
stream.close() 


#stream.close()
#ventana=Ventana()
#ventana.crearVentana()
#ventana.crearFrameInicio()