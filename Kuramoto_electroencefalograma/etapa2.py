from edfreader import EDFreader
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.fft import fft, rfft
from scipy.fft import fftfreq, rfftfreq
from scipy.signal import butter,filtfilt
import xlrd


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

def para_orden(angulo):
    vec=0;
    for i in range(np.size(angulo)):
        vec=vec + np.cos(angulo[i])+1.j*np.sin(angulo[i])
    alpha=np.angle(vec/np.size(angulo))
    r=abs(vec)
    return [alpha,r]


def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 0.5 * fs 
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y


directorio = r"C:\Users\mateo\Downloads\python\Trabajo_epilepsia\Registros\\"
#Lectura de datos en excel
excel = xlrd.open_workbook("resumen_archivos.xls")
hoja=excel.sheet_by_index(0)
#lectura de los archivos
for registro_n in range(hoja.nrows):
    filename=directorio+hoja[registro_n][0].value+'.edf'
    hdl = EDFreader(filename)

    ncanales=hdl.getNumSignals() #Cantidad de canales

    sampling_rate=int(hdl.getSampleFrequency(s=0)) #Muestras por segundo
    #Buffer para extraer una porción del registro
    buffer=np.zeros((sampling_rate*int(hoja[registro_n][3].value),ncanales))
    ##Llenar el buffer con cada canal del registro desde la posicion deseada
    for n_canal in range(ncanales):
        #Para cada archivo se se toma 10seg antes del ataque
        hdl.fseek(s=n_canal,offset=(int(hoja[registro_n][1].value)-10)*sampling_rate,whence=hdl.EDFSEEK_SET)
        hdl.readSamples(n_canal, buffer[:,n_canal], sampling_rate*int(hoja[registro_n][3].value))
        
    #Dibujar los datos
    z_signals=zScore(buffer)
    plt.figure(1,figsize=(20,10))
    plt.suptitle('Paciente '+hoja[registro_n][0].value[0:5]+' Registro Nro '+hoja[registro_n][0].value[6:8])
    gs = gridspec.GridSpec(2, 2)
    ax1 = plt.subplot(gs[:,0])
    ax1.set_title("EEG")
    ax1.set_ylabel("Electroencefalograma")
    ax1.set_xlabel("Tiempo [s]")
    ax2 = plt.subplot(gs[0,1])
    ax2.set_title("FFT")
    ax2.set_ylabel("Amplitud")
    ax2.set_xlabel("Frecuencia [rad/s]")
    ax3 = plt.subplot(gs[1,1])
    ax3.set_title("Parametro de orden r")
    ax3.set_ylabel("Amplitud [pu]")
    ax3.set_xlabel("Numero de muestra")
    for n_canal in range(ncanales):
        k=0
        r=np.zeros(np.shape(z_signals[:,n_canal]))
        alpha=np.zeros(np.shape(z_signals[:,n_canal]))
        barrido=64 #t=64/256
        tamanio_muestra=5*sampling_rate
        while(k+tamanio_muestra<=sampling_rate*int(hoja[registro_n][3].value)):
            furier = fft(z_signals[k:k+tamanio_muestra,n_canal]);
            #amp=abs(furier)
            angulo=np.angle(furier)
            parametro= para_orden(angulo)
            r[k:k+tamanio_muestra]= (r[k:k+tamanio_muestra] + parametro[1]*np.ones(tamanio_muestra))/2
            alpha[k:k+tamanio_muestra] = (alpha[k:k+tamanio_muestra] + parametro[0]*np.ones(tamanio_muestra))/2
            k=k+barrido

        #r_filtrado= butter_lowpass_filter(r,1,sampling_rate,2)
        #alpha_filtrado= butter_lowpass_filter(alpha,1,sampling_rate,2)
        tiempo=np.linspace(1/sampling_rate,int(hoja[registro_n][3].value),sampling_rate*int(hoja[registro_n][3].value))
        #Dibujo de cada canal
        #eeg
        ax1.plot(tiempo,z_signals[:,n_canal]+8*n_canal)
        #fft
        yf=fft(z_signals[:,n_canal])
        y=2*n_canal+np.abs(yf[0:np.size(z_signals[:,n_canal])//15])/max(np.abs(yf[0:np.size(z_signals[:,n_canal])]))
        xf=fftfreq(np.size(z_signals[:,n_canal]),sampling_rate)
        x=2*np.pi*(max(tiempo)**2)*sampling_rate*xf[0:np.size(xf)//15]
        ax2.plot(x,y)
        #parámetro de orden
        ax3.plot(tiempo,r+0.5*n_canal)
    plt.savefig(hoja[registro_n][0].value+'_'+str(registro_n)+'.png')
    plt.close()
    #cálculo del promedio de cada paciente de todos los canales
    plt.figure(2,figsize=(20,10))
    plt.suptitle('Paciente '+hoja[registro_n][0].value[0:5]+' Registro Nro '+hoja[registro_n][0].value[6:8])
    gs = gridspec.GridSpec(2, 2)
    ax1 = plt.subplot(gs[:,0])
    ax1.set_title("EEG")
    ax1.set_ylabel("Electroencefalograma")
    ax1.set_xlabel("Tiempo [s]")
    ax2 = plt.subplot(gs[0,1])
    ax2.set_title("FFT")
    ax2.set_ylabel("Amplitud")
    ax2.set_xlabel("Frecuencia [rad/s]")
    ax3 = plt.subplot(gs[1,1])
    ax3.set_title("Parametro de orden r")
    ax3.set_ylabel("Amplitud [pu]")
    ax3.set_xlabel("Numero de muestra")
    tamanio=np.shape(z_signals)
    promedio=sum(np.transpose(z_signals))/tamanio[1]
    promedio_filtrado= butter_lowpass_filter(promedio,30,sampling_rate,2)
    k=0
    r=np.zeros(np.shape(promedio_filtrado))
    alpha=np.zeros(np.shape(promedio_filtrado))
    barrido=64
    tamanio_muestra=5*sampling_rate
    while(k+tamanio_muestra<=sampling_rate*int(hoja[registro_n][3].value)):
        furier = fft(promedio_filtrado[k:k+tamanio_muestra]);
        #amp=abs(furier)
        angulo=np.angle(furier)
        parametro= para_orden(angulo)
        r[k:k+tamanio_muestra]= (r[k:k+tamanio_muestra] + parametro[1]*np.ones(tamanio_muestra))/2
        alpha[k:k+tamanio_muestra] = (alpha[k:k+tamanio_muestra] + parametro[0]*np.ones(tamanio_muestra))/2
        k=k+barrido
        
    #r_filtrado= butter_lowpass_filter(r,1,sampling_rate,2)
    #alpha_filtrado= butter_lowpass_filter(alpha,1,sampling_rate,2)
    tiempo=np.linspace(1/sampling_rate,int(hoja[registro_n][3].value),sampling_rate*int(hoja[registro_n][3].value))
    ax1.plot(tiempo,promedio_filtrado)
    yf=fft(promedio_filtrado)
    y=2*n_canal+np.abs(yf[0:np.size(z_signals[:,n_canal])//15])/max(np.abs(yf[0:np.size(z_signals[:,n_canal])]))
    xf=fftfreq(np.size(z_signals[:,n_canal]),sampling_rate)
    x=2*np.pi*(max(tiempo)**2)*sampling_rate*xf[0:np.size(xf)//15]
    ax2.plot(x,y)
        
    x=np.linspace(0,np.size(r),np.size(r))
    ax3.plot(tiempo,r)
    plt.savefig(hoja[registro_n][0].value+'_'+str(registro_n)+' Promediado'+'.png')
    plt.close()

