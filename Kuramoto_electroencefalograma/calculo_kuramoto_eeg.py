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

directorio = r"C:\Users\mateo\OneDrive\Documentos\python\Trabajo_epilepsia\\"
nombre_registro='chb01_15.edf'

filename=directorio+nombre_registro
hdl = EDFreader(filename)

ncanales=hdl.getNumSignals() #Cantidad de canales

sampling_rate=int(hdl.getSampleFrequency(s=0)) #Muestras por segundo
#Buffer para extraer una porción del registro
buffer=np.zeros((sampling_rate*30,ncanales))
##Llenar el buffer con cada canal del registro desde la posicion deseada
for n_canal in range(ncanales):
    #Para el archivo chb01_15.edf el ataque inicia en 1732, así que tomamos desde el 1722
    hdl.fseek(s=n_canal,offset=sampling_rate,whence=hdl.EDFSEEK_SET)
    hdl.readSamples(n_canal, buffer[:,n_canal], sampling_rate*30)
    
#Dibujar los datos
z_signals=zScore(buffer)
n=220
r=np.zeros([np.size(z_signals[:,0])//n,ncanales])
alpha=np.zeros([np.size(z_signals[:,0])//n,ncanales])
#for l in range (ncanales):
l=0
kn=0
for k in range(n,np.size(z_signals[:,l]),np.size(z_signals[:,l])//n):
    #print(l)
    #print(z_signals[kn:k,l])
    furier = fft(z_signals[kn:k,l]);
    amp=abs(furier)
    angulo=np.angle(furier)
    vec=0;
    for i in range(np.size(angulo)):
        vec=vec + np.cos(angulo[i])+1.j*np.sin(angulo[i])
    alpha[(k-n)//n,l]=np.angle(vec)
    r[(k-n)//n,l]=abs(vec)
    kn=k
tiempo=np.linspace(1/sampling_rate,30,sampling_rate*30)
#for l in range (ncanales):        
    #plt.figure(1)
plt.subplot(311)
plt.plot(range(np.size(alpha[:,l])),180*alpha[:,l]/np.pi+360*l)
plt.title("ángulo alpha")
plt.ylabel("Angulo °")
#plt.figure(2)
plt.subplot(312)
plt.plot(range(np.size(r[:,l])),r[:,l]+30*l)
plt.title("Amplitud r")
plt.ylabel("Amplitud")
#plt.figure(3)
plt.subplot(313)
plt.plot(tiempo,z_signals[:,l]+5*l)
plt.title("Señale electro encefalograma")
plt.ylabel("Señal")
plt.show()


##for n_canal in range(ncanales):
##    #plt.subplot(211)
##    plt.plot(tiempo,z_signals[:,n_canal]+5*n_canal) #Sumado 5*n_canal para dibujar a distinto y
##    print(z_signals[:,n_canal])
##    yf=fft(z_signals[:,n_canal])
##    xf=fftfreq(np.size(z_signals[:,n_canal]),sampling_rate)
##    #plt.figure(n_canal)
##    #plt.plot(xf, 5*n_canal+2.0/np.size(z_signals[:,n_canal]) * np.abs(yf[0:np.size(z_signals[:,n_canal])]))
##plt.show()
