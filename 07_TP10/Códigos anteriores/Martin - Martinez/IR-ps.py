import tkinter
from tkinter import ttk
from tkinter import filedialog
import os
import Main as Main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from xlsxwriter import Workbook


mainW = tkinter.Tk() #ventana principal
mainW.title('IR-ps') #nombre del programa: Impulse Response Processing Software
mainW.geometry('600x550')

tab_control = ttk.Notebook(mainW) #control de las pestañas

#crea las 3 pestañas

firstTab = ttk.Frame(tab_control)
secondTab = ttk.Frame(tab_control)
thirdTab = ttk.Frame(tab_control)

#nombra las 3 pestañas de la ventana principal y las caracteriza

#primera pestaña

def switchSS(): #encendido y apagado de los botones según se selecciona SS o IR

    if fminLabel['state'] == 'disable':
        fminLabel['state'] = 'active'
        entryFmin['state'] = 'active'
        fmaxLabel['state'] = 'active'
        entryFmax['state'] = 'active'
        duracLabel['state'] = 'active'
        entryDurac['state'] = 'active'
        bLog['state'] = 'active'
        bLin['state'] = 'active'
    else:
        fminLabel['state'] = 'normal'
        entryFmin['state'] = 'normal'
        fmaxLabel['state'] = 'normal'
        entryFmax['state'] = 'normal'
        duracLabel['state'] = 'normal'
        entryDurac['state'] = 'normal'
        bLog['state'] = 'normal'
        bLin['state'] = 'normal'


def switchIR():

    fminLabel['state'] = 'disabled'
    entryFmin['state'] = 'disabled'
    fmaxLabel['state'] = 'disabled'
    entryFmax['state'] = 'disabled'
    duracLabel['state'] = 'disabled'
    entryDurac['state'] = 'disabled'
    bLog['state'] = 'disabled'
    bLin['state'] = 'disabled'


def import_file():  # Ventana para seleccionar el archivo (IR o SS)
    # Obtiene el path del archivo seleccionado

    global filename
    global path

    path = filedialog.askopenfilename(
        title='Open a file',
        filetypes=[("WAV Files", "*.wav")])

    # Obtiene el nombre del archivo sin el path

    filename = os.path.basename(path)
    bFileName.config(text = filename)

tab_control.add(firstTab, text='SS/IR File') #pestañas

fileSect = tkinter.LabelFrame(firstTab, text=" Select the file type: ")
fileSect.pack(pady=10)

b0=tkinter.IntVar(fileSect) #b0 es la variable que designa si el archivo es un SS o IR
b0.set(0)

bSS = tkinter.Radiobutton(fileSect, text="Sine Sweep", width = 10,command =switchSS,value =0, variable = b0) #boton SS
bSS.grid(row=0, column=0,padx=10, pady = 10)

bIR = tkinter.Radiobutton(fileSect,text="IR", width = 10, command = switchIR,value =1, variable = b0) #botón IR
bIR.grid(row=0, column=1,padx=10, pady = 10)

bFile = tkinter.Button(fileSect,text="Load File", width = 10, command = import_file) #botón de carga
bFile.grid(row=0, column=2,padx=10, pady = 10)

bFileLabel = tkinter.Label(fileSect,text="File:", width = 10) #Display del nombre del archivo
bFileLabel.grid(row=1, column=0,padx=10, pady = 10)

bFileName = tkinter.Label(fileSect,text='No file selected', width = 40,bg="white",
                          relief=tkinter.GROOVE, height = 1) #Display del nombre del archivo
bFileName.grid(row=1, column=1,padx=10, pady = 10, columnspan=2)

monoOrSt = tkinter.LabelFrame(firstTab, text=" Is the file mono or stereo? ")
monoOrSt.pack(pady=10)

b1=tkinter.IntVar(monoOrSt) #b1 es la variable que designa si el audio es mono o estéreo
b1.set(0)


def IACCbuttonOff():    #encendido y apagado de los botones de IACC según archivo mono o estéreo

    if bIACC['state'] == 'normal':
        bIACC['state'] = 'disabled'
        bIACCe['state'] = 'disabled'
        bIACCl['state'] = 'disabled'

    else:
        bIACC['state'] = 'disabled'
        bIACCe['state'] = 'disabled'
        bIACCl['state'] = 'disabled'

def IACCbuttonOn():

    if bIACC['state'] == 'disable':
        bIACC['state'] = 'normal'
        bIACCe['state'] = 'normal'
        bIACCl['state'] = 'normal'

    else:

        bIACC['state'] = 'normal'
        bIACCe['state'] = 'normal'
        bIACCl['state'] = 'normal'

bSt = tkinter.Radiobutton(monoOrSt,value = 1,variable=b1 ,text="Stereo", width = 8, command = IACCbuttonOn) #botón estereo
bSt.grid(row=1, column=2,padx=10, pady = 10)

bMono = tkinter.Radiobutton(monoOrSt,value = 0 ,variable=b1, text = "Mono", width = 8, command = IACCbuttonOff) #boton mono
bMono.grid(row=1, column=1,padx=10, pady = 10)

ifSS = tkinter.LabelFrame(firstTab, text=" Please, enter the following data about the SS file: ")
ifSS.pack(pady=10)

b2=tkinter.IntVar(ifSS) #b1 es la variable que designa si el sweep es lineal o logarítmico
b2.set(0)

#etiquetas y botones de los datos para cargar las frecuencias

fminLabel = tkinter.Label(ifSS, text=" Min. Freq [Hz]: (default 20 Hz) ", wraplength = 120)
entryFmin = tkinter.Entry(ifSS) #Valor de la frecuencia mínima
tkinter.Entry.insert(entryFmin,-1, 20)
fmaxLabel = tkinter.Label(ifSS, text=" Max. Freq [Hz]: (default 20 kHz) ", wraplength = 120)
entryFmax = tkinter.Entry(ifSS) #Valor de la frecuencia máxima
tkinter.Entry.insert(entryFmax,-1, 20000)
duracLabel = tkinter.Label(ifSS, text=" Duration [s]: (default 5 s)", wraplength = 90)
entryDurac = tkinter.Entry(ifSS) #Valor de la frecuencia duración
tkinter.Entry.insert(entryDurac,-1, 5)
bLin = tkinter.Radiobutton(ifSS,value = 0 ,text="Linear", width = 8,variable=b2)
bLog = tkinter.Radiobutton(ifSS,value = 1 ,text="Logarithmic", width = 12, variable=b2)

fminLabel.grid(row=0, column=0,padx=10, pady = 10)
entryFmin.grid(row=0, column=2,padx=10, pady = 10)
fmaxLabel.grid(row=1, column=0,padx=10, pady = 10)
entryFmax.grid(row=1, column=2,padx=10, pady = 10)
duracLabel.grid(row=2, column=0,padx=10, pady = 10)
entryDurac.grid(row=2, column=2,padx=10, pady = 10)
bLin.grid(row=3, column=0,padx=10, pady = 10)
bLog.grid(row=3, column=2,padx=10, pady = 10)

#segunda pestaña
tab_control.add(secondTab, text='Representation')

octTer = tkinter.LabelFrame(secondTab, text="Select if you want the results to be in 1/1 octaves or 1/3 octaves: ")
octTer.pack(pady=10)

b3 = tkinter.IntVar(octTer) #b3 es la variable que designa si la representación es por octava o tercio
b3.set(0)

bOct = tkinter.Radiobutton(octTer,value = 0,variable=b3 ,text="1/1 Octave", width = 20) #botón Octava
bOct.grid(row=0, column=0,padx=10, pady = 10)

bToct = tkinter.Radiobutton(octTer,value = 1 ,variable=b3, text = "1/3 Octave", width = 20) #boton Tercio
bToct.grid(row=0, column=1,padx=10, pady = 10)

IACClabel = tkinter.LabelFrame(secondTab, text="IACC parameters: ") # sección de cálculo del IACC
IACClabel.pack(pady=10)

b4 = tkinter.IntVar(IACClabel) #b4 es la variable que designa la selección de IACC, IACCe e IACCl
b4.set(0)

bIACC = tkinter.Radiobutton(IACClabel,value = 0,variable=b4 ,text="IACC", width = 8) #botón IACC
bIACC.grid(row=0, column=0,padx=5, pady = 10)
bIACC['state'] = 'disable'

bIACCe = tkinter.Radiobutton(IACClabel,value = 1 ,variable=b4, text = "IACCe", width = 8) #boton IACCe
bIACCe.grid(row=0, column=1,padx=5, pady = 10)
bIACCe['state'] = 'disable'

bIACCl = tkinter.Radiobutton(IACClabel,value = 2 ,variable=b4, text = "IACCl", width = 8) #boton IACCl
bIACCl.grid(row=0, column=2,padx=5, pady = 10)
bIACCl['state'] = 'disable'

NRA= tkinter.LabelFrame(secondTab, text=" Smoothing: ")
NRA.pack(pady=10)

b5 = tkinter.IntVar(NRA) #b5 es la variable que designa si la reducción de ruido es MMF o Schroeder
b5.set(1)

bSch = tkinter.Radiobutton(NRA,value = 1 ,variable=b5, text = "Schroeder", width = 10) #boton Schroeder
despCompLabel = tkinter.Label(NRA, text=" Bgnd noise compensation ") #Metodo de compensación de ruido de fondo
bDespComp = ttk.Combobox(NRA, values = ['No compensation', 'Lundeby', 'Chu']) #botón lista desplegable compensación
bDespComp.current([0])

bMMF = tkinter.Radiobutton(NRA,value = 0,variable=b5 ,text="MMF", width = 10) #botón MMF
MMFLabel = tkinter.Label(NRA, text=" Time window [ms]: (default 50 ms) ", wraplength = 120) #ventana temporal para el MMF
entryMMF = tkinter.Entry(NRA) #Valor de la ventana temporal para el MMF
tkinter.Entry.insert(entryMMF,-1, 50) #pone default 50 ms

bMMF.grid(row=0, column=0,padx=8, pady = 10)
MMFLabel.grid(row=0, column=1,padx=8, pady = 10)
entryMMF.grid(row=0, column=2,padx=8, pady = 10)
bSch.grid(row=1, column=0,padx=8, pady = 10)
despCompLabel.grid(row=1, column=1,padx=8, pady = 10)
bDespComp.grid(row=1, column=2,padx=8, pady = 10)

def main():

    """
    Esta función es la encargada de calcular parámetros y generar la ventana secundaria
    con los gráficos y los datos de salida
    :return:
    """

    if bFileName.cget("text") == 'No file selected':
        bSentryName.config(text='Please, remember to select a file', bg = 'red')
        return()

    bSentryName.config(text='Calculating...',bg="white") #cambio de descripción del label

    #se obtiene la información de los botones para entregarsela a las funciones

    select = b0.get()
    monoOrestereo = b1.get()
    file = path
    f1 = entryFmin.get()
    f2 = entryFmax.get()
    D = entryDurac.get()
    st = b2.get()
    OctavaOTercio = b3.get()
    m = entryMMF.get()
    b22 = b5.get()
    comp = bDespComp.get()
    b44 = b4.get()

    if monoOrestereo == 0:

        IRrep, IRre1kSuave, IRre1k, fs, EDT, T20,\
        T30, C50, C80, EDTt, Tt, Ts = Main.Main(select, monoOrestereo, file, f1,
                                                f2, D, st, OctavaOTercio, m, b22, comp, b44)

    elif monoOrestereo == 1:
        IRrep, IRre1kSuave, IRre1k, fs, EDT, T20,\
        T30, C50, C80, EDTt, Tt, Ts, IACC = Main.Main(select,monoOrestereo, file, f1,
                                                      f2, D, st, OctavaOTercio, m, b22, comp,b44)

    bSentryName.config(text='Done!',bg ='#38EB5C') #cambio de descripción del label

    #Ventana emergente secundaria

    graphW = tkinter.Toplevel()
    mainW.iconify()
    widthWin = graphW.winfo_screenwidth()
    heightWin = graphW.winfo_screenheight()
    graphW.geometry("%dx%d" % (widthWin, heightWin-100))
    graphW.title("Data output")

    #genera la figura

    fig = Figure(figsize=(4, 3), dpi=100)
    t = np.arange(0,len(IRre1k)/fs,1/fs)
    if len(t) == len(IRre1k) + 1:
        t = t[:-1]
    elif len(t) + 1 == len(IRre1k):
        IRre1k = IRre1k[:-1]

    ax = fig.add_subplot()
    IRre1k = IRre1k / np.max(IRre1k)
    IRre1k = 20 * np.log10(abs(IRre1k) + 0.00001)
    ax.plot(t,IRre1k, label = 'Impulse response')
    ax.plot(t, IRre1kSuave,label = 'Smooth IR')
    ax.legend()
    ax.grid()
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Relative Amplitude [dB]')
    ax.set_xlim([0,len(IRre1k)/fs])
    ax.set_ylim([-80,10])
    plt.show()

    #Canvas es una funcion de tkinter para hacer los plots

    canvas = FigureCanvasTkAgg(fig, master=graphW)  # CREAR AREA DE DIBUJO DE TKINTER.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    # Crea tabla

    scrollbar = tkinter.Scrollbar(graphW, orient='horizontal')
    scrollbar.pack(side=tkinter.TOP,fill = tkinter.X)

    tv = ttk.Treeview(graphW, height=6, xscrollcommand = scrollbar.set)

    # Ahora se divide para entregar resultados en bandas o tercios de octava

    if OctavaOTercio == 0: # Bandas de Octavas

        # Define formato de columnas

        tv['columns'] = ('Parameter','31.5','63','125','250','500','1.000','2.000','4.000','8.000','16.000')
        tv.column('#0', width=0, stretch=tkinter.NO)
        tv.column('Parameter', anchor=tkinter.CENTER, width=80)
        tv.column('31.5', anchor=tkinter.CENTER, width=80)
        tv.column('63', anchor=tkinter.CENTER, width=80)
        tv.column('125', anchor=tkinter.CENTER, width=80)
        tv.column('250', anchor=tkinter.CENTER, width=80)
        tv.column('500', anchor=tkinter.CENTER, width=80)
        tv.column('1.000', anchor=tkinter.CENTER, width=80)
        tv.column('2.000', anchor=tkinter.CENTER, width=80)
        tv.column('4.000', anchor=tkinter.CENTER, width=80)
        tv.column('8.000', anchor=tkinter.CENTER, width=80)
        tv.column('16.000', anchor=tkinter.CENTER, width=80)

    # Define contenido de columnas

        tv.heading('#0', text='', anchor=tkinter.CENTER)
        tv.heading('Parameter', text='Parameter', anchor=tkinter.CENTER)
        tv.heading('31.5', text='31.5 [Hz]', anchor=tkinter.CENTER)
        tv.heading('63', text='63 [Hz]', anchor=tkinter.CENTER)
        tv.heading('125', text='125 [Hz]', anchor=tkinter.CENTER)
        tv.heading('250', text='250 [Hz]', anchor=tkinter.CENTER)
        tv.heading('500', text='500 [Hz]', anchor=tkinter.CENTER)
        tv.heading('1.000', text='1 [kHz]', anchor=tkinter.CENTER)
        tv.heading('2.000', text='2 [kHz]', anchor=tkinter.CENTER)
        tv.heading('4.000', text='4 [kHz]', anchor=tkinter.CENTER)
        tv.heading('8.000', text='8 [kHz]', anchor=tkinter.CENTER)
        tv.heading('16.000', text='16 [kHz]', anchor=tkinter.CENTER)

    # Define contenido de filas

        tv.insert(parent='', index=0, iid=0, text='',
                  values=('EDT [s]', EDT[0], EDT[1], EDT[2], EDT[3], EDT[4], EDT[5], EDT[6], EDT[7], EDT[8], EDT[9]))
        tv.insert(parent='', index=1, iid=1, text='',
                  values=('T20 [s]', T20[0],T20[1],T20[2],T20[3],T20[4],T20[5],T20[6],T20[7],T20[8],T20[9]))
        tv.insert(parent='', index=2, iid=2, text='',
                  values=('T30 [s]', T30[0],T30[1],T30[2],T30[3],T30[4],T30[5],T30[6],T30[7],T30[8],T30[9]))
        tv.insert(parent='', index=3, iid=3, text='',
                  values=('C50 [dB]', C50[0],C50[1],C50[2],C50[3],C50[4],C50[5],C50[6],C50[7],C50[8],C50[9]))
        tv.insert(parent='', index=4, iid=4, text='',
                  values=('C80 [dB]', C80[0],C80[1],C80[2],C80[3],C80[4],C80[5],C80[6],C80[7],C80[8],C80[9]))
        tv.insert(parent='', index=5, iid=5, text='',
                  values=('EDTt [s]', EDTt[0],EDTt[1],EDTt[2],EDTt[3],EDTt[4],EDTt[5],EDTt[6],EDTt[7],EDTt[8],EDTt[9]))
        tv.insert(parent='', index=6, iid=6, text='',
                  values=('Tt [s]', Tt[0],Tt[1],Tt[2],Tt[3],Tt[4],Tt[5],Tt[6],Tt[7],Tt[8],Tt[9]))
        tv.insert(parent='', index=7, iid=7, text='',
                  values=('Ts [ms]', Ts[0],Ts[1],Ts[2],Ts[3],Ts[4],Ts[5],Ts[6],
                          Ts[7],Ts[8],Ts[9]))

        if monoOrestereo == 1: # Si es estereo agrega IACC a la tabla

            # Elige etiqueta de fila según se seleccionó IACC, IACCe o IACCl
            if b4.get() == 0:
                nameIACC = 'IACC'
            elif b4.get() == 1:
                nameIACC = 'IACCe'
            elif b4.get() == 2:
                nameIACC = 'IACCl'

            tv.insert(parent='', index=8, iid=8, text='',
                values = (nameIACC, IACC[0],IACC[1],IACC[2],IACC[3],IACC[4],IACC[5],IACC[6],IACC[7],IACC[8],IACC[9]))

        tv.pack(fill=tkinter.BOTH, expand=1)

    else:   # Bandas de Tercios de Octavas

        tv['columns'] = ('Parameter', '20', '25', '31.5', '40', '50', '63', '80', '100', '125', '160'
                        , '200', '250', '315', '400', '500', '630', '800', '1000', '1250', '1600'
                         , '2000', '2500', '3150', '4000', '5000', '6300', '8000', '10000', '12500'
                         , '16000', '20000')

        tv.column('#0', width=0, stretch=tkinter.NO)
        tv.column('Parameter', anchor=tkinter.CENTER, width=80)
        tv.column('20', anchor=tkinter.CENTER, width=80)
        tv.column('25', anchor=tkinter.CENTER, width=80)
        tv.column('31.5', anchor=tkinter.CENTER, width=80)
        tv.column('40', anchor=tkinter.CENTER, width=80)
        tv.column('50', anchor=tkinter.CENTER, width=80)
        tv.column('63', anchor=tkinter.CENTER, width=80)
        tv.column('80', anchor=tkinter.CENTER, width=80)
        tv.column('100', anchor=tkinter.CENTER, width=80)
        tv.column('125', anchor=tkinter.CENTER, width=80)
        tv.column('160', anchor=tkinter.CENTER, width=80)
        tv.column('200', anchor=tkinter.CENTER, width=80)
        tv.column('250', anchor=tkinter.CENTER, width=80)
        tv.column('315', anchor=tkinter.CENTER, width=80)
        tv.column('400', anchor=tkinter.CENTER, width=80)
        tv.column('500', anchor=tkinter.CENTER, width=80)
        tv.column('630', anchor=tkinter.CENTER, width=80)
        tv.column('800', anchor=tkinter.CENTER, width=80)
        tv.column('1000', anchor=tkinter.CENTER, width=80)
        tv.column('1250', anchor=tkinter.CENTER, width=80)
        tv.column('1600', anchor=tkinter.CENTER, width=80)
        tv.column('2000', anchor=tkinter.CENTER, width=80)
        tv.column('2500', anchor=tkinter.CENTER, width=80)
        tv.column('3150', anchor=tkinter.CENTER, width=80)
        tv.column('4000', anchor=tkinter.CENTER, width=80)
        tv.column('5000', anchor=tkinter.CENTER, width=80)
        tv.column('6300', anchor=tkinter.CENTER, width=80)
        tv.column('8000', anchor=tkinter.CENTER, width=80)
        tv.column('10000', anchor=tkinter.CENTER, width=80)
        tv.column('12500', anchor=tkinter.CENTER, width=80)
        tv.column('16000', anchor=tkinter.CENTER, width=80)
        tv.column('20000', anchor=tkinter.CENTER, width=80)

        # Define contenido de columnas

        tv.heading('#0', text='', anchor=tkinter.CENTER)
        tv.heading('Parameter', text='Parameter', anchor=tkinter.CENTER)
        tv.heading('20', text='20 [Hz]', anchor=tkinter.CENTER)
        tv.heading('25', text='25 [Hz]', anchor=tkinter.CENTER)
        tv.heading('31.5', text='31.5 [Hz]', anchor=tkinter.CENTER)
        tv.heading('40', text='40 [Hz]', anchor=tkinter.CENTER)
        tv.heading('50', text='50 [Hz]', anchor=tkinter.CENTER)
        tv.heading('63', text='63 [Hz]', anchor=tkinter.CENTER)
        tv.heading('80', text='80 [Hz]', anchor=tkinter.CENTER)
        tv.heading('100', text='100 [Hz]', anchor=tkinter.CENTER)
        tv.heading('125', text='125 [Hz]', anchor=tkinter.CENTER)
        tv.heading('160', text='160 [Hz]', anchor=tkinter.CENTER)
        tv.heading('200', text='200 [Hz]', anchor=tkinter.CENTER)
        tv.heading('250', text='250 [Hz]', anchor=tkinter.CENTER)
        tv.heading('315', text='315 [Hz]', anchor=tkinter.CENTER)
        tv.heading('400', text='400 [Hz]', anchor=tkinter.CENTER)
        tv.heading('500', text='500 [Hz]', anchor=tkinter.CENTER)
        tv.heading('630', text='630 [Hz]', anchor=tkinter.CENTER)
        tv.heading('800', text='800 [Hz]', anchor=tkinter.CENTER)
        tv.heading('1000', text='1.00 [kHz]', anchor=tkinter.CENTER)
        tv.heading('1250', text='1.25 [kHz]', anchor=tkinter.CENTER)
        tv.heading('1600', text='1.60 [kHz]', anchor=tkinter.CENTER)
        tv.heading('2000', text='2.00 [kHz]', anchor=tkinter.CENTER)
        tv.heading('2500', text='2.50 [kHz]', anchor=tkinter.CENTER)
        tv.heading('3150', text='3.15 [kHz]', anchor=tkinter.CENTER)
        tv.heading('4000', text='4.00 [kHz]', anchor=tkinter.CENTER)
        tv.heading('5000', text='5.00 [kHz]', anchor=tkinter.CENTER)
        tv.heading('6300', text='6.30[kHz]', anchor=tkinter.CENTER)
        tv.heading('8000', text='8.00 [kHz]', anchor=tkinter.CENTER)
        tv.heading('10000', text='10.00 [kHz]', anchor=tkinter.CENTER)
        tv.heading('12500', text='12.50 [kHz]', anchor=tkinter.CENTER)
        tv.heading('16000', text='16.00 [kHz]', anchor=tkinter.CENTER)
        tv.heading('20000', text='20.00 [kHz]', anchor=tkinter.CENTER)

        # Define contenido de filas

        tv.insert(parent='', index=0, iid=0, text='',
                  values=('EDT [s]', EDT[0], EDT[1], EDT[2], EDT[3], EDT[4], EDT[5], EDT[6], EDT[7], EDT[8], EDT[9]
                          , EDT[10], EDT[11], EDT[12], EDT[13], EDT[14], EDT[15], EDT[16], EDT[17], EDT[18], EDT[18], EDT[19]
                          , EDT[20], EDT[21], EDT[22], EDT[23], EDT[24], EDT[25], EDT[26], EDT[27], EDT[28], EDT[29], EDT[30]))
        tv.insert(parent='', index=1, iid=1, text='',
                  values=('T20 [s]', T20[0], T20[1], T20[2], T20[3], T20[4], T20[5], T20[6], T20[7], T20[8], T20[9]
                          , T20[10], T20[11], T20[12], T20[13], T20[14], T20[15], T20[16], T20[17], T20[18], T20[18], T20[19]
                          , T20[20], T20[21], T20[22], T20[23], T20[24], T20[25], T20[26], T20[27], T20[28], T20[29], T20[30]))
        tv.insert(parent='', index=2, iid=2, text='',
                  values=('T30 [s]', T30[0], T30[1], T30[2], T30[3], T30[4], T30[5], T30[6], T30[7], T30[8], T30[9]
                          , T30[10], T30[11], T30[12], T30[13], T30[14], T30[15], T30[16], T30[17], T30[18], T30[18], T30[19]
                          , T30[20], T30[21], T30[22], T30[23], T30[24], T30[25], T30[26], T30[27], T30[28], T30[29], T30[30]))
        tv.insert(parent='', index=3, iid=3, text='',
                  values=('C50 [dB]', C50[0], C50[1], C50[2], C50[3], C50[4], C50[5], C50[6], C50[7], C50[8], C50[9]
                          , C50[10], C50[11], C50[12], C50[13], C50[14], C50[15], C50[16], C50[17], C50[18], C50[18], C50[19]
                          , C50[20], C50[21], C50[22], C50[23], C50[24], C50[25], C50[26], C50[27], C50[28], C50[29], C50[30]))
        tv.insert(parent='', index=4, iid=4, text='',
                  values=('C80 [dB]', C80[0], C80[1], C80[2], C80[3], C80[4], C80[5], C80[6], C80[7], C80[8], C80[9]
                          , C80[10], C80[11], C80[12], C80[13], C80[14], C80[15], C80[16], C80[17], C80[18], C80[18], C80[19]
                          , C80[20], C80[21], C80[22], C80[23], C80[24], C80[25], C80[26], C80[27], C80[28], C80[29], C80[30]))
        tv.insert(parent='', index=5, iid=5, text='',
                  values=('EDTt [s]', EDTt[0], EDTt[0], EDTt[1], EDTt[2], EDTt[3], EDTt[4], EDTt[5], EDTt[6], EDTt[7], EDTt[8], EDTt[9]
                          , EDTt[10], EDTt[11], EDTt[12], EDTt[13], EDTt[14], EDTt[15], EDTt[16], EDTt[17], EDTt[18], EDTt[18], EDTt[19]
                          , EDTt[20], EDTt[21], EDTt[22], EDTt[23], EDTt[24], EDTt[25], EDTt[26], EDTt[27], EDTt[28], EDTt[29], EDTt[30]))
        tv.insert(parent='', index=6, iid=6, text='',
                  values=('Tt [s]', Tt[0], Tt[1], Tt[2], Tt[3], Tt[4], Tt[5], Tt[6], Tt[7], Tt[8], Tt[9]
                          , Tt[10], Tt[11], Tt[12], Tt[13], Tt[14], Tt[15], Tt[16], Tt[17], Tt[18], Tt[18], Tt[19]
                          , Tt[20], Tt[21], Tt[22], Tt[23], Tt[24], Tt[25], Tt[26], Tt[27], Tt[28], Tt[29], Tt[30]))
        tv.insert(parent='', index=7, iid=7, text='',
                  values=('Ts [s]', Ts[0], Ts[1], Ts[2], Ts[3], Ts[4], Ts[5], Ts[6], Ts[7], Ts[8], Ts[9]
                          , Ts[10], Ts[11], Ts[12], Ts[13], Ts[14], Ts[15], Ts[16], Ts[17], Ts[18], Ts[18], Ts[19]
                          , Ts[20], Ts[21], Ts[22], Ts[23], Ts[24], Ts[25], Ts[26], Ts[27], Ts[28], Ts[29], Ts[30]))

        if monoOrestereo == 1:  # Si es estereo agrega IACC

            # Elige etiqueta de fila según se seleccionó IACC, IACCe o IACCl
            if b4.get() == 0:
                nameIACC = 'IACC'
            elif b4.get() == 1:
                nameIACC = 'IACCe'
            elif b4.get() == 2:
                nameIACC = 'IACCl'

            tv.insert(parent='', index=8, iid=8, text='',
                      values=(nameIACC, IACC[0], IACC[1], IACC[2], IACC[3], IACC[4], IACC[5], IACC[6], IACC[7], IACC[8], IACC[9]
                          ,IACC[10], IACC[11], IACC[12], IACC[13], IACC[14], IACC[15], IACC[16], IACC[17], IACC[18], IACC[18], IACC[19]
                          ,IACC[20], IACC[21], IACC[22], IACC[23], IACC[24], IACC[25], IACC[26], IACC[27], IACC[28], IACC[29], IACC[30]))
        tv.pack(fill=tkinter.BOTH, expand=1)
        scrollbar.config(command=tv.xview)

    # Funciones encargadas de exportar la a Excel y Cerrar el programa (funcionalidades de botones)

    def create_xlsx_file(file_path: str, headers: dict, items: list): # Crea archivo excel
        with Workbook(file_path) as workbook:
            worksheet = workbook.add_worksheet()
            worksheet.write_row(row=0, col=0, data=headers.values())
            header_keys = list(headers.keys())
            for index, item in enumerate(items):
                row = map(lambda field_id: item.get(field_id, ''), header_keys)
                worksheet.write_row(row=index + 1, col=0, data=row)


    def excelExport():  # Da formato a la información para poder ser exportado correctamente

        # Abre dialogo para selec. path de exportación
        ruta = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Excel Export")
        ruta = ruta + '.xlsx'

        # Trae los parámetros del Main
        if monoOrestereo == 0:

            IRrep, IRre1kSuave, IRre1k, fs, EDT, T20, \
            T30, C50, C80, EDTt, Tt, Ts = Main.Main(select, monoOrestereo, file, f1,
                                                    f2, D, st, OctavaOTercio, m, b22, comp, b44)

        elif monoOrestereo == 1:
            IRrep, IRre1kSuave, IRre1k, fs, EDT, T20, \
            T30, C50, C80, EDTt, Tt, Ts, IACC = Main.Main(select, monoOrestereo, file, f1,
                                                          f2, D, st, OctavaOTercio, m, b22, comp, b44)

            # Elige etiqueta de fila según se seleccionó IACC, IACCe o IACCl
            if b4.get() == 0:
                nameIACC = 'IACC'
            elif b4.get() == 1:
                nameIACC = 'IACCe'
            elif b4.get() == 2:
                nameIACC = 'IACCl'


        # Ordena los datos para exportar
        if OctavaOTercio == 0: # Si es con Bandas de Octava

            # Primero se arman las columnas:
            parameters = ['EDT [s]', 'T20 [s]', 'T30 [s]', 'C50 [dB]', 'C80[dB]', 'EDTt [s]', 'Tt [s]', 'Ts [s]',nameIACC]
            headers = {'Parameter':'Parameter','31.5':'31.5 [Hz]','63':'63 [Hz]','125':'125 [Hz]','250':'250 [Hz]'
                ,'500':'500 [Hz]','1.000':'1.000 [Hz]','2.000':'2.000 [Hz]','4.000':'4.000 [Hz]',
                '8.000':'8.000 [Hz]','16.000':'16.000 [Hz]'}

            if monoOrestereo == 0: # Si es mono crea IACC con "-"
                IACC = []
                for i in range(len(EDT)):
                    IACC.append('-')

            banda1 = [EDT[0],T20[0],T30[0],C50[0],C80[0], EDTt[0], Tt[0], Ts[0], IACC[0]]
            banda2 = [EDT[1], T20[1], T30[1], C50[1], C80[1], EDTt[1], Tt[1], Ts[1], IACC[1]]
            banda3 = [EDT[2], T20[2], T30[2], C50[2], C80[2], EDTt[2], Tt[2], Ts[2], IACC[2]]
            banda4 = [EDT[3], T20[3], T30[3], C50[3], C80[3], EDTt[3], Tt[3], Ts[3], IACC[3]]
            banda5 = [EDT[4], T20[4], T30[4], C50[4], C80[4], EDTt[4], Tt[4], Ts[4], IACC[4]]
            banda6 = [EDT[5], T20[5], T30[5], C50[5], C80[5], EDTt[5], Tt[5], Ts[5], IACC[5]]
            banda7 = [EDT[6], T20[6], T30[6], C50[6], C80[6], EDTt[6], Tt[6], Ts[6], IACC[6]]
            banda8 = [EDT[7], T20[7], T30[7], C50[7], C80[7], EDTt[7], Tt[7], Ts[7], IACC[7]]
            banda9 = [EDT[8], T20[8], T30[8], C50[8], C80[8], EDTt[8], Tt[8], Ts[8], IACC[8]]
            banda10 = [EDT[9], T20[9], T30[9], C50[9], C80[9], EDTt[9], Tt[9], Ts[9], IACC[9]]

            # Define los items que se van a exportar en filas
            items = []
            for i in range(len(parameters)):

                items.append({'Parameter': parameters[i], '31.5': banda1[i], '63': banda2[i], '125':banda3[i], '250': banda4[i]
                              , '500': banda5[i], '1.000': banda6[i],  '2.000': banda7[i],  '4.000': banda8[i],  '8.000': banda9[i]
                              ,  '16.000': banda10[i]})

        else: # Si es con bandas de Tercios de Octava

            # Primero se arman las columnas:

            parameters = ['EDT [s]', 'T20 [s]', 'T30 [s]', 'C50 [dB]', 'C80[dB]', 'EDTt [s]', 'Tt [s]', 'Ts [s]','IACC']
            headers = {'Parameter': 'Parameter','20':'20 [Hz]', '25': '25 [Hz]', '31.5': '31.5 [Hz]', '40': '40 [Hz]',
                       '50': '50 [Hz]', '63': '63 [Hz]', '80': '80 [Hz]', '100': '100 [Hz]', '125': '125 [Hz]',
                       '160': '160 [Hz]', '200': '200 [Hz]', '250': '250 [Hz]', '315': '315 [Hz]', '400': '400 [Hz]',
                       '500': '500 [Hz]', '630': '630 [Hz]', '800': '800 [Hz]', '1.000': '1.000 [Hz]',
                     '1.250': '1.250 [Hz]', '1.600': '1.600 [Hz]', '2.000': '2.000 [Hz]','2.500': '2.500 [Hz]',
                     '3.150': '3.150 [Hz]', '4.000': '4.000 [Hz]', '5.000': '5.000 [Hz]', '6.300': '6.300 [Hz]',
                       '8.000': '8.000 [Hz]','10.000': '10.000 [Hz]', '12.500': '12.500 [Hz]', '16.000': '16.000 [Hz]',
                       '20.000': '20.000 [Hz]'}

            if monoOrestereo == 0: # Si es mono crea IACC con "-"
                IACC = []
                for i in range(len(EDT)):
                    IACC.append('-')

            banda1 = [EDT[0], T20[0], T30[0], C50[0], C80[0], EDTt[0], Tt[0], Ts[0], IACC[0]]
            banda2 = [EDT[1], T20[1], T30[1], C50[1], C80[1], EDTt[1], Tt[1], Ts[1], IACC[1]]
            banda3 = [EDT[2], T20[2], T30[2], C50[2], C80[2], EDTt[2], Tt[2], Ts[2], IACC[2]]
            banda4 = [EDT[3], T20[3], T30[3], C50[3], C80[3], EDTt[3], Tt[3], Ts[3], IACC[3]]
            banda5 = [EDT[4], T20[4], T30[4], C50[4], C80[4], EDTt[4], Tt[4], Ts[4], IACC[4]]
            banda6 = [EDT[5], T20[5], T30[5], C50[5], C80[5], EDTt[5], Tt[5], Ts[5], IACC[5]]
            banda7 = [EDT[6], T20[6], T30[6], C50[6], C80[6], EDTt[6], Tt[6], Ts[6], IACC[6]]
            banda8 = [EDT[7], T20[7], T30[7], C50[7], C80[7], EDTt[7], Tt[7], Ts[7], IACC[7]]
            banda9 = [EDT[8], T20[8], T30[8], C50[8], C80[8], EDTt[8], Tt[8], Ts[8], IACC[8]]
            banda10 = [EDT[9], T20[9], T30[9], C50[9], C80[9], EDTt[9], Tt[9], Ts[9], IACC[9]]
            banda11 = [EDT[10], T20[10], T30[10], C50[10], C80[10], EDTt[10], Tt[10], Ts[10], IACC[10]]
            banda12 = [EDT[11], T20[11], T30[11], C50[11], C80[11], EDTt[11], Tt[11], Ts[11], IACC[11]]
            banda13 = [EDT[12], T20[12], T30[12], C50[12], C80[12], EDTt[12], Tt[12], Ts[12], IACC[12]]
            banda14 = [EDT[13], T20[13], T30[13], C50[13], C80[13], EDTt[13], Tt[13], Ts[13], IACC[13]]
            banda15 = [EDT[14], T20[14], T30[14], C50[14], C80[14], EDTt[14], Tt[14], Ts[14], IACC[14]]
            banda16 = [EDT[15], T20[15], T30[15], C50[15], C80[15], EDTt[15], Tt[15], Ts[15], IACC[15]]
            banda17 = [EDT[16], T20[16], T30[16], C50[16], C80[16], EDTt[16], Tt[16], Ts[16], IACC[16]]
            banda18 = [EDT[17], T20[17], T30[17], C50[17], C80[17], EDTt[17], Tt[17], Ts[17], IACC[17]]
            banda19 = [EDT[18], T20[18], T30[18], C50[18], C80[18], EDTt[18], Tt[18], Ts[18], IACC[18]]
            banda20 = [EDT[19], T20[19], T30[19], C50[19], C80[19], EDTt[19], Tt[19], Ts[19], IACC[19]]
            banda21 = [EDT[20], T20[20], T30[20], C50[20], C80[20], EDTt[20], Tt[20], Ts[20], IACC[20]]
            banda22 = [EDT[21], T20[21], T30[21], C50[21], C80[21], EDTt[21], Tt[21], Ts[21], IACC[21]]
            banda23 = [EDT[22], T20[22], T30[22], C50[22], C80[22], EDTt[22], Tt[22], Ts[22], IACC[22]]
            banda24 = [EDT[23], T20[23], T30[23], C50[23], C80[23], EDTt[23], Tt[23], Ts[23], IACC[23]]
            banda25 = [EDT[24], T20[24], T30[24], C50[24], C80[24], EDTt[24], Tt[24], Ts[24], IACC[24]]
            banda26 = [EDT[25], T20[25], T30[25], C50[25], C80[25], EDTt[25], Tt[25], Ts[25], IACC[25]]
            banda27 = [EDT[26], T20[26], T30[26], C50[26], C80[26], EDTt[26], Tt[26], Ts[26], IACC[26]]
            banda28 = [EDT[27], T20[27], T30[27], C50[27], C80[27], EDTt[27], Tt[27], Ts[27], IACC[27]]
            banda29 = [EDT[28], T20[28], T30[28], C50[28], C80[28], EDTt[28], Tt[28], Ts[28], IACC[28]]
            banda30 = [EDT[29], T20[29], T30[29], C50[29], C80[29], EDTt[29], Tt[29], Ts[29], IACC[29]]
            banda31 = [EDT[30], T20[30], T30[30], C50[30], C80[30], EDTt[30], Tt[30], Ts[30], IACC[30]]

            # Define los items que se van a exportar en filas
            items = []
            for i in range(len(parameters)):
                # suma medio segundo y unos pocos Hz para que la detección no esté tan ajustada

                items.append(
                    {'Parameter': parameters[i],'20':banda1[i], '25': banda2[i], '31.5': banda3[i], '40': banda4[i],
                       '50': banda5[i], '63': banda6[i], '80': banda7[i], '100': banda8[i], '125': banda9[i],
                       '160': banda10[i], '200': banda11[i], '250': banda12[i], '315': banda13[i], '400': banda14[i],
                       '500': banda15[i], '630': banda16[i], '800': banda17[i], '1.000': banda18[i],
                     '1.250': banda19[i], '1.600': banda20[i], '2.000': banda21[i],'2.500': banda22[i],
                     '3.150': banda23[i], '4.000': banda24[i], '5.000': banda25[i], '6.300': banda26[i],
                       '8.000': banda27[i],'10.000': banda28[i], '12.500': banda29[i], '16.000': banda30[i],
                       '20.000': banda31[i]})
        try: # Envía la información a ser exportada...
            create_xlsx_file(ruta, headers, items)
            bExpLabel.config(text = 'File created' )

        except:
            bExpLabel.config(text='Error. Please, try again')

    def cerrar(): # Botón return, funcionalidad para volver a la venta principal
        mainW.deiconify()
        graphW.destroy()
        bSentryName.config(text='',bg ='white')

    button = tkinter.Button(graphW, text="Return", command=cerrar, width = 20)  # botón para volver a ventana principal
    button.pack(side=tkinter.RIGHT, pady = 10, padx = 10)

    bExport = tkinter.Button(graphW, text="Export", command=excelExport, width = 20)  # botón de exportar a excel
    bExport.pack(side=tkinter.LEFT, pady = 10, padx = 10)

    bExpLabel = tkinter.Label(graphW, text='', width=40, bg="white",relief=tkinter.GROOVE)  # Estado de la creación del achivo
    bExpLabel.pack(pady=15, side=tkinter.LEFT)

bCalc = tkinter.Button(secondTab,text="Calculate!", width = 10,command = main) #botón de cálculo
bCalc.pack(pady = 10)

bStatusLabel = tkinter.Label(secondTab,text="Status:", width = 10) #Display del nombre del archivo
bStatusLabel.pack(pady = 10)

bSentryName = tkinter.Label(secondTab,text='', width = 40,bg="white",
                          relief=tkinter.GROOVE, height = 1) #Display del nombre del archivo
bSentryName.pack(pady = 10)

#tercera pestaña

tab_control.add(thirdTab, text='About')
labelNC = tkinter.Label(thirdTab, text= 'IR-ps or Impulse Response Processing Software is a software developed by Gaspar '
                                        'Bevilacqua, Tomás Martín and Ciro Martínez in the context of the subject '
                                        'Acoustical Instruments and Measurements of the Sound Engineering career, '
                                        'in UNTREF, Argentina.',wraplength = 400)

labelInst = tkinter.Label(thirdTab, text= 'INSTRUCTIONS: First, in "SS/IR File" tab, you need to load the file containing '
                                        'the recording of the Sine Sweep, or the Impulse response. Then, select if the '
                                        'file is mono or stereo. If the file is a SS, you will need to give the '
                                        'requested information in order to process the file. Next, you will have to '
                                        'go to "representation" tab in order to choose if the results will be '
                                        'represented in 1/1 octave or 1/3 octave bands. Also, you will have to select '
                                        'which IACC parameter you want to obtain. Last, the smoothing algotithm is '
                                        'selected. MMF or Schroeder methods are available. For Schroeder '
                                        'there are 3 options for background noise compensation (no compensation, '
                                        "Lundeby and Chu's methods). When selecting MMF, you must enter the window "
                                        'size in milliseconds (preset by default at 50 ms). Finally, you have to click '
                                        'Calculate! button and now you can access to the results',wraplength = 400)

labelOut = tkinter.Label(thirdTab, text= 'Outputs: Once clicking the Calculate! button, the results are displayed in a '
                                         'new window called Data Output. A graph of the IR is shown in the upper part '
                                         'and in  a table in de lower with different parameters. For mono signals, EDT,'
                                         ' T20, T30, C50, C80, EDTt, Tt and Ts parameters are calculated. For the case '
                                         'of stereo signals, the mono parameters are calculated from the average '
                                         "between both channels and it's obtain the IACC parameter too. In addition, "
                                         'the results can be exported to an excel file by clicking '
                                         'Export',wraplength = 400)
labelNC.pack( pady = 5)
labelInst.pack( pady = 5)
labelOut.pack(pady = 5)

#general

tab_control.pack(expand=1, fill='both') #este comando es para que se hagan efectivas las pestañas
mainW.mainloop()

