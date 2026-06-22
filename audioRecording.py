import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

sampleRate = 16000
Time = 4
recording = sd.rec(int(Time * sampleRate), samplerate=sampleRate, channels=1, dtype=np.int16)
sd.wait()
write('Winki_MiniProject.wav', sampleRate, recording)