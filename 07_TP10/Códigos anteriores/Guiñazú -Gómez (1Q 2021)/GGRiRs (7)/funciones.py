import scipy.signal
from scipy.signal import chirp
import scipy as sp
from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.ndimage import median_filter

np.seterr(divide='ignore', invalid='ignore')

# Se cean los array con las frecuencias centrales de los bancos de filtro
bandas_octavas = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
bandas_tercios = [25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250,
                  315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000,
                  5000, 6300, 8000, 10000, 12500, 16000, 20000]


# Funcion para generar filtro inverso a partir de los parametros ingresados por el usuario
def generar_filtro(parametros_filtro):
    canales = parametros_filtro[0]
    metodo = parametros_filtro[1]
    f_inicio = parametros_filtro[2]
    f_fin = parametros_filtro[3]
    duracion = parametros_filtro[4]
    fs = parametros_filtro[5]
    t = np.linspace(0, duracion, duracion * fs)
    filtros = []
    for canal in range(canales):  # Se crea un filtro por cada canal de la señal

        if metodo == 0:  # Se pregunta si el filtro inverso tiene que ser lineal o logaritmico
            sine = chirp(t, f_inicio, duracion, f_fin, method='linear')  # Se crea sine-sweep lineal

            filtro = np.flip(sine)  # Se voltea en el eje temporal para obtener filtro inverso

        else:
            w1 = 2 * np.pi * f_inicio  # Se calculan variables que servirán para la modulación del filtro invero
            w2 = 2 * np.pi * f_fin
            T = duracion
            K = (T * w1) / (np.log(w2 / w1))
            L = T / (np.log(w2 / w1))

            w = (K / L) * np.exp((t / L))
            m = w1 / (2 * np.pi * w)

            sine = chirp(t, f_inicio, duracion, f_fin, method='logarithmic')  # Se crea sine-sweep logarítmico
            filtro = m * np.flip(
                sine)  # Se multiplica el sine-sweep invertido en tiempo por la modulación de la envolvente
            filtro = filtro / max(filtro)  # Se normaliza

        filtros.append(filtro)

    return filtros


# Funcion para calcular la respuesta al impulso a partir del sine sweep grabado importado por el usuario
# y el filtro inverso generado
def rir(sine_grabado, filtro_inverso):
    rirs = []
    for i in range(len(filtro_inverso)):  # Se genera una rir por canal de la señal
        rir = sp.signal.fftconvolve(sine_grabado[i], filtro_inverso[i])  # Se covolucionan ambas señales
        rir = rir[np.argmax(rir):]  # Se toma la porcion util de la señal
        rirfinal = rir / abs(max(rir))  # Se normaliza
        rirs.append(rirfinal)

    return rirs


# Función para obtener los datos de los archivos de audio importados
def promediado_seniales(seniales):
    stereo = []
    fs = 0

    data, fs = sf.read(seniales)
    try:  # Si es estereo se reordena el array
        stereo.append(data[:, 0])
        stereo.append(data[:, 1])
    except:
        stereo.append(data)  # Si es mono se deja como está

    return fs, stereo


# Funcion para filtrar la señal por octavas o tercios de octavas
def filtrado(senial, fs, fraccion_octavas, orden):
    senial_filtrada = []

    G = 10 ** (3 / 10)  # Se obtienen los límites de las bandas segun la norma ISO-8832

    if fraccion_octavas == 1:
        bandas = bandas_octavas
        lim_inf = G ** (-1 / 2)
        lim_sup = G ** (1 / 2)
    else:
        bandas = bandas_tercios
        lim_inf = G ** (-1 / 6)
        lim_sup = G ** (1 / 6)
    for i, banda in enumerate(bandas):
        sup = lim_sup * banda / (0.5 * fs)  # Se aplican los límites a cada banda

        if sup >= 1:
            sup = 0.999999
        inf = lim_inf * banda / (0.5 * fs)

        filtro = sp.signal.butter(orden, [inf, sup], 'bp', output='sos')  # Se crea filtro Buttterworth
        filtrado = sp.signal.sosfilt(filtro, senial)  # Se realiza el filtrado

        senial_filtrada.append(filtrado[:int(len(filtrado) * 0.95)])  # Se toma la porción util de la señal

    return senial_filtrada


# Función de Lundeby para obtener el límite de la integral inversa de Schoreder
def lundeby(senial, fs):
    tds = []

    for banda in senial:  # Se realiza el proceso para cada banda
        ventana = round(0.01 * fs)  # Se define una ventana de 10ms
        maximo = np.argmax(banda)
        banda = banda[maximo:]  # Se recorta la señal a partir del sonido directo
        vector_rms = np.zeros(len(banda))
        ruido_rms = np.mean(banda[int(len(banda) * 0.8):int(len(banda) * 0.9)])  # Se calcula el nivel de ruido como el
        # valor medio del último 10% de la señal
        for i in range(0, int(len(banda)), ventana):  # Se obtienen los valores medios de la señal en cada ventana
            valor_rms = np.mean(banda[i:i + ventana])
            vector_rms[i:i + ventana] = valor_rms

        xmas5 = np.argwhere(vector_rms <= ruido_rms + 5)  # Se busca el primer punto donde el nivel sea 5dB mayor al
        # nivel de ruido
        if xmas5.size == 0:
            xmas5 = np.argwhere(vector_rms <= ruido_rms)

        x5_ruido = np.ndarray.item(xmas5[0])

        X = np.arange(0, x5_ruido)
        Y = banda[0:x5_ruido]

        a = linregress(X, Y)
        x = np.arange(0, len(banda))
        y = a.slope * x + a.intercept  # Se realiza una regresión lineal entre el punto x5_ruido
        # y el máximo de la señal
        ruido = np.empty(len(x))
        ruido.fill(ruido_rms)

        td = int((ruido_rms - a.intercept) / a.slope)  # Se busca el punto donde se intercepta esta regersión y
        # el nivel de ruido
        if td < 0:
            td = int(len(banda) * 0.5)

        max = y[0]

        x10_1 = np.argwhere(y <= max - 10)  # Se busca el punto donde la señal se atenue 10 dB
        if x10_1.size == 0 or x10_1[0] == 0:
            ventana = round(0.01 * fs)
        else:
            x10 = np.ndarray.item(x10_1[0])
            ventana = int(x10 / 5)  # Se crea una nueva ventana para obtener la media de la señal
            # En este caso van a existir 5 ventanas por cada vez que la señal disminuya 10 dB

        vector_rms2 = np.zeros(len(banda))

        for i in range(0, int(len(banda)), ventana):
            valor_rms = np.mean(banda[i:i + ventana])  # Se vuelve a calcular el vector con los valores rms de la señal
            # obtenidos con la ventana
            vector_rms2[i:i + ventana] = valor_rms

        td_viejo = td + 1000
        i = 0
        while np.abs(
                td - td_viejo) > 0.001 * fs and i <= 4:  # Comienda la iteración. El máximo de iteración se fijó en 5
            # a partir de lo expresado en el paper de Lundeby

            td_viejo = td

            ruidomenos5_1 = np.argwhere(vector_rms2 <= ruido_rms - 5)  # Se toma el primer punto 5dB por debajo del
            # nivel de ruido
            if ruidomenos5_1.size == 0:
                ruido_rms2 = np.mean(vector_rms2[int(len(vector_rms2) * 0.8):int(len(vector_rms2) * 0.9)])
            else:
                ruidomenos5 = np.ndarray.item(ruidomenos5_1[0])
                ruido_rms2 = np.mean(vector_rms2[ruidomenos5:])

            xmas5_2 = np.argwhere(y <= ruido_rms2 + 5)  # Se toma el primer punto 5dB por encima del nivel de ruido
            if xmas5_2.size == 0 or xmas5_2[0] == 0:
                break
            x5_ruido2 = np.ndarray.item(xmas5_2[0])

            xmas25 = np.argwhere(y <= ruido_rms2 + 30)  # Se toma el primer punto 30dB por emcima del nivel de ruido
            if xmas25.size == 0 or xmas25[0] == 0:
                break

            x25_ruido2 = np.ndarray.item(xmas25[0])

            X2 = np.arange(x25_ruido2, x5_ruido2)
            Y2 = vector_rms2[x25_ruido2:x5_ruido2]

            a2 = linregress(X2, Y2)
            x2 = np.arange(0, len(banda))
            y2 = a2.slope * x2 + a2.intercept  # Se realiza una regresión lineal entre los puntos
            # +5dB y +25dB encontrados
            ruido = np.empty(len(x2))
            ruido.fill(ruido_rms2)

            td = int((ruido_rms2 - a2.intercept) / a2.slope)  # Se busca el punto donde se interceptan esta recta
            # y el nivel de ruido

            y = y2
            ruido_rms = ruido_rms2
            i = i + 1

        if td >= len(banda) or td < 0:
            td = int(len(banda) * 0.9)

        tds.append(td)

    return tds


# Función para calcular la integral de Schoreder con el límite obtenido en Lundeby
def schoeder(senial, td):
    sch_final = []
    for i, banda in enumerate(senial):  # Se realiza la integral para cada banda

        sch = np.cumsum(banda[td[i]::-1] ** 2)[td[i]::-1]  # Integral inversa
        sch = 10 * np.log10(sch / np.max(sch))  # Paso a energía
        sch_final.append(sch)

    return sch_final


# Función para calcular la mediana movil a partir de la ventana definida por el usuario
def mediana_movil(senial, td, ventana):
    medianas = []

    for i, banda in enumerate(senial):  # Se realiza para cada banda
        banda_recortada = banda[np.argmax(banda):]
        mediana = median_filter(banda_recortada[0:td[i]], ventana)  # Mediana movil
        mediana = mediana - max(mediana)  # Normalizacion
        medianas.append(mediana)

    return medianas


# Función para calcular la energía de la señal
def energy(senial):
    etcs = []
    for banda in senial:
        etc = 10 * np.log10(banda ** 2)  # Energía
        etcs.append(etc)
    return etcs


# Función para calcular los parametros EDT, T20 y T30
def parametros(senial, fs):
    EDT = []
    T20 = []
    T30 = []

    for i, banda in enumerate(senial):

        x5_1 = np.argwhere(banda[np.argmax(banda):] <= -5)  # Se busca el punto -5dB del máximo de la señal
        if x5_1.size == 0:
            x5 = 0
        else:
            x5 = np.ndarray.item(x5_1[0])

        x10_1 = np.argwhere(banda[np.argmax(banda):] <= -10)  # Se busca el punto -10dB del máximo de la señal
        if x10_1.size == 0:
            x10 = np.argmin(banda)
        else:
            x10 = np.ndarray.item(x10_1[0])

        x25_1 = np.argwhere(banda[np.argmax(banda):] <= -25)  # Se busca el punto -25dB del máximo de la señal
        if x25_1.size == 0:
            x25 = np.argmin(banda)
        else:
            x25 = np.ndarray.item(x25_1[0])

        x35_1 = np.argwhere(banda[np.argmax(banda):] <= -35)  # Se busca el punto -35dB del máximo de la señal
        if x35_1.size == 0:
            x35 = np.argmin(banda)
        else:
            x35 = np.ndarray.item(x35_1[0])

        xEDT = np.arange(0, x10)
        coeff_EDT = np.polyfit(xEDT, banda[0:x10], 1)  # Se realiza una regresión lineal entre los puntos
        # 0dB y -10dB
        t_EDT = (-60 - coeff_EDT[1]) / (coeff_EDT[0] * fs)  # Se calcula el EDT a partir de la regresión

        xT20 = np.arange(x5, x25)
        coeff_T20 = np.polyfit(xT20, banda[x5:x25], 1)  # Se realiza una regresión lineal entre los puntos
        # -5dB y -25dB
        t_T20 = (-60 - coeff_T20[1]) / (coeff_T20[0] * fs)  # Se calcula el T20 a partir de la regresión

        xT30 = np.arange(x5, x35)
        coeff_T30 = np.polyfit(xT30, banda[x5:x35], 1)  # Se realiza una regresión lineal entre los puntos
        # -5dB y -35dB
        t_T30 = (-60 - coeff_T30[1]) / (coeff_T30[0] * fs)  # Se calcula el T30 a partir de la regresión

        EDT.append(t_EDT)
        T20.append(t_T20)
        T30.append(t_T30)

    return EDT, T20, T30


# Función para obtener el C50 y C80
def claridad(senial, fs, td):
    c50 = []
    c80 = []

    for i, banda in enumerate(senial):
        banda_max = banda[np.argmax(banda):]
        h2 = banda_max ** 2  # Energía de la señal
        t50 = int(fs * 50 / 1000)  # Muestras dentro de 50ms
        t80 = int(fs * 80 / 1000)  # Muestras dentro de 80ms

        c5 = 10 * np.log10(np.sum(h2[:t50]) / np.sum(h2[t50:td[i]]))  # C50
        c8 = 10 * np.log10(np.sum(h2[:t80]) / np.sum(h2[t80:td[i]]))  # C80

        c50.append(c5)
        c80.append(c8)

    return c50, c80


# Funcion para calcular el transition Time
def transitiontime(senial, fs):
    tt = []

    for banda in senial:
        p2 = banda ** 2  # Energía de la señal
        maximo = np.argmax(p2)
        banda_max = p2[maximo:]
        i = 0

        while banda_max[i + 1] <= banda_max[i]:
            i = i + 1

        banda_tt = banda_max[i:]  # Se saca el sonido directo de la señal

        E = np.sum(banda_tt)

        j = 1
        sumatoria = np.cumsum(banda_tt)  # Suma acumulativa de la energía
        while sumatoria[j] <= 0.9 * E:  # Se toma el Tt como el punto donde la suma acumulativa es igual al 90% de la
            # energía de la señal
            j = j + 1

        tt_banda = j + i

        tts = (tt_banda / fs) * 1000  # Pasaje de muestras a ms

        tt.append(tts)

    return tt


# Función para caular el EDTt
def earlyDecayTT(senial, tt, fs):
    EDTt = []

    tt1 = np.divide(tt, 1000)
    tt2 = np.multiply(tt1, fs)  # Paso el Tt a muestras

    for i, banda in enumerate(senial):

        tts = int(tt2[i])
        if tt2[i] > len(banda):
            tts = len(banda)

        xEDTt = np.arange(0, tts)

        yEDTt = banda[0:tts]
        coeff_EDTt = linregress(xEDTt, yEDTt)  # Realizo regresión lineal entre los puntos 0dB y el transition time
        t_EDTt = (-60 - coeff_EDTt.intercept) / (coeff_EDTt.slope * fs)  # EDTt

        EDTt.append(t_EDTt)

    return EDTt


# Función para calcular el IACC para audios estereo
def IACC(L, R, fs):
    IACC_early = []

    for i in range(len(R)):

        t80 = int(fs * 80 / 1000)  # Muestras en 80ms
        IACF = []
        for tau in range(int(-0.001*fs),int(0.001*fs), int(0.001*fs/10)):

            if tau >= 0:
                IACFi = np.sum(L[i][0:t80] * R[i][tau:t80 + tau]) / \
                        np.sqrt((np.sum(L[i][0:t80] ** 2)) * (np.sum(R[i][0:t80] ** 2)))
            else:
                tau = abs(tau)
                IACFi = np.sum(R[i][0:t80] * L[i][tau:t80 + tau]) / \
                        np.sqrt((np.sum(R[i][0:t80] ** 2)) * (np.sum(L[i][0:t80] ** 2)))



            IACF.append(IACFi)

        IACCi = max(IACF)

        IACC_early.append(abs(IACCi))
        
    return IACC_early


# Ploteo de la energía de la señal y el correspondiente suavizado
def ploteo_banda(senial, suavisado, fs, W, H):
    plt.clf()
    px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
    fig = plt.figure(figsize=(W * px, H * px))
    ax = fig.add_subplot(111)

    x_senial = np.arange(0, len(senial) / fs, 1 / fs)
    x_suavisado = np.arange(0, len(suavisado) / fs, 1 / fs)

    if len(x_senial) == len(senial) + 1:
        x_senial = x_senial[:-1]
    if len(x_suavisado) == len(suavisado) + 1:
        x_suavisado = x_suavisado[:-1]
    ax.plot(x_senial, senial)
    ax.plot(x_suavisado, suavisado + max(senial))
    ax.set_xlabel('Tiempo [s]')
    ax.set_ylabel('dBFS')
    plt.tight_layout()

    return fig