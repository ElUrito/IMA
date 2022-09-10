import numpy as np
import matplotlib.pyplot as plt

def moving_average(x, w):
    """ 
    x: input signal
    w: window
    """
    resultado = np.convolve(x, np.ones(w), 'valid') / w
    plt.plot(resultado)
    if __name__ != "__main__":
        plt.show()
    return resultado

