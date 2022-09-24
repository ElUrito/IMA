import scipy.signal
import numpy as np
import soundfile as sf


def gen_sweep():
    sample_rate = 48000
    fmin = 50
    fmax = 12000
    duration = 12
    t = np.arange(0, int(duration * sample_rate)) / sample_rate


    # Generador de sweep y filtro inv
    log_signal = scipy.signal.chirp(t, f0=fmin, f1=fmax, t1=duration, method='logarithmic')
    loginv_signal = log_signal[::-1]


    # Guardado de sweep y filtro inverso en wav
    sf.write('sine_sweep.wav', log_signal, sample_rate)
    sf.write('inv_filter.wav', loginv_signal, sample_rate)


