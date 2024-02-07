#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:17:06 2023

@author: felipe
"""
from edfreader import EDFreader
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, rfft
from scipy.fft import fftfreq, rfftfreq


def zScore(X,mu=None, sigma=None):
    #Obtener el z-score canal por canal. 
    if mu is None and sigma is None:
        y=X-X.mean(axis=0,keepdims=True)
        y=y/X.std(axis=0,keepdims=True)
    elif sigma is None:
    #Obetener el z-score con una desviacion estandar común (Se suele usar la de todos los registros y todos los canales)
        y=X-X.mean(axis=0,keepdims=True)    
        y=y/sigma
    else:
    #Obtener el z-score con una media y deviación estándar común
        y=(X-mu)/sigma
    return y

directorio = r"C:\Users\mateo\Downloads\python\Trabajo_epilepsia\Registros"
nombre_registro=['\chb01_03.edf','\chb01_04.edf','\chb01_15.edf','\chb01_16.edf','\chb01_18.edf',
                 '\chb01_21.edf','\chb01_26.edf','\chb02_16+.edf','\chb02_19.edf','\chb03_01.edf','\chb03_02.edf',
                 '\chb03_03.edf','\chb03_04.edf','\chb03_34.edf','\chb03_35.edf','\chb03_36.edf'
                 ,'\chb04_05.edf','\chb04_08.edf','\chb04_28.edf','\chb05_06.edf'
                 ,'\chb05_13.edf','\chb05_16.edf','\chb05_17.edf','\chb05_22.edf']
canal=['FP1-F7','F7-T7','T7-P7','P7-O1','FP1-F3','F3-C3','C3-P3','P3-O1','FP2-F4','F4-C4','C4-P4','P4-O2'
       ,'FP2-F8','F8-T8','T8-P8','P8-O2','FZ-CZ','CZ-PZ','P7-T7','T7-FT9','FT9-FT10','FT10-T8','T8-P8','ECG']

for n_register in range(len(nombre_registro)):
    filename=directorio+nombre_registro[n_register]
    hdl = EDFreader(filename)

    ncanales=hdl.getNumSignals() #Cantidad de canales

    sampling_rate=int(hdl.getSampleFrequency(s=0)) #Muestras por segundo
    #Buffer para extraer una porción del registro
    tiempo_total=int((hdl.getFileDuration() or "")*1e-9)
    buffer=np.zeros((sampling_rate*tiempo_total,ncanales))
    ##Llenar el buffer con cada canal del registro desde la posicion deseada
    for n_canal in range(ncanales):
        hdl.fseek(s=n_canal,offset=sampling_rate,whence=hdl.EDFSEEK_SET)
        hdl.readSamples(n_canal, buffer[:,n_canal], sampling_rate*tiempo_total)
        
    #Dibujar los datos
    z_signals=zScore(buffer)
    tiempo=np.linspace(1/sampling_rate,tiempo_total,sampling_rate*tiempo_total)
    plt.figure(n_register,figsize=(20,8))
    for n_canal in range(ncanales):
        plt.subplot(121)
        plt.plot(tiempo,z_signals[:,n_canal]+5*n_canal,label=(canal[n_canal])) #Sumado 5*n_canal para dibujar a distinto y
        plt.legend()
        plt.title('Paciente '+nombre_registro[n_register][1:6]+' Registro '+nombre_registro[n_register][7:9])
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Ondas eeg')
        yf=fft(z_signals[:,n_canal])
        y=2*n_canal+np.abs(yf[0:np.size(z_signals[:,n_canal])//15])/max(np.abs(yf[0:np.size(z_signals[:,n_canal])]))
        xf=fftfreq(np.size(z_signals[:,n_canal]),sampling_rate)
        x=(max(tiempo)**2)*sampling_rate*xf[0:np.size(xf)//15];
        plt.subplot(122)
        plt.plot(x,y,label=canal[n_canal])
        plt.legend()
        plt.title('Paciente '+nombre_registro[n_register][1:6]+' Registro '+nombre_registro[n_register][7:9]+' FFT')
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Ondas eeg')
    plt.savefig(nombre_registro[n_register][1:9]+'.png')
    plt.close()
#plt.show()





