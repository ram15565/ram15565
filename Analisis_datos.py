# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:22:57 2017

@author: Victor Tzorin
"""

#Programa que encuentra la cantidad de muones verticales en un intervalo de tiempo dado

#Importación de librerías

#----------------------------------------------------------------------------------------------------------#

import bz2
import math
import numpy as np
from datetime import *
from matplotlib.pyplot import *
from scipy.misc import derivative
from scipy.optimize import fsolve

#Inicio del programa

print("\n")
print(datetime.now())
print("\n")

#Datos a ingresar

#----------------------------------------------------------------------------------------------------------#

#Ingresar nombre general de archivos ".dat"
fname="chrisY"

#Ingresar fecha inicial de datos con el formato YYYY_MM_DD_HHhMM
sdate = datetime.strptime("2018_02_09_23h00","%Y_%m_%d_%Hh%M")

#Ingresar fecha final de datos con el formato YYYY_MM_DD_HHhMM
edate = datetime.strptime("2018_02_10_02h00","%Y_%m_%d_%Hh%M")

#Ingresar canal de adquisicion
chnnl=1

#Ingresar los bins a considerar
bsize = 1

#Ingresar el máximo adcq a aceptar
madcq = 1600

#Ingresar el intervalo de tiempo a analizar
intvl=1

#Radio del tanque (metros)
derad=0.41

#Altura del tanque (metros)
dehei=1.14

#Ingresar nombre de archivo final
rfnam="CHR1" 
 
#Calculos previos

#----------------------------------------------------------------------------------------------------------#
 
#Intervalo de tiempo en segundos
dtime=(edate-sdate)

#Generalizacion para uno o varios archivos
if dtime.days==0 and dtime.seconds==0:
    
    dtime=dtime+timedelta(0,3600)
    
else:
    
    pass

#Intervalo de tiempo en horas
dhour=int((dtime.days*24)+(dtime.seconds)/3600)


#Ciclo que recorre todos los archivos

#----------------------------------------------------------------------------------------------------------#

#Fecha actual
cdate=sdate

#Bins totales
tbins = madcq/bsize

#Bins que hay
data1=[]

for i in range(tbins):
    
    data1.append(i*bsize+bsize)
    

#Arreglo de cantidad de eventos por bins
data2 = np.zeros((tbins)).tolist()

#Carga integrada de eventos por hora
data3=[]

#Carga acumulada
chrg1=0

#Cargas de eventos de flujo vertical de muones
data6=[]

#Contador de eventos de flujo vertical de muones variable
data7=[]

#Suma de eventos muonicos
data8=[]

#Ciclo que recorre todos los archivos
for i in range(0,dhour):
    
    try:
        
        #Lectura del archivo comprimido
        dfile = bz2.BZ2File(str(fname)+"_nogps_"+cdate.strftime("%Y_%m_%d_%Hh%M")+".dat.bz2")
    
        #Ciclo que lee cada línea de los archivos
        for cline in dfile:
            
            #fin de evento y cuenta de reloj
            if(cline.startswith("# t")):  
                
                data3.append(chrg1)
                chrg1=0
        
            #Suma de carga
            elif(not cline.startswith("#")):
                
                if int(cline.split(" ")[chnnl-1])>50:
                    
                    chrg1=chrg1+int(cline.split(" ")[chnnl-1])-50
                else:
                    
                    pass
            
            else:
                
                pass
        
        #Analisis de acuerdo a los intervalos de tiempo definidos
        if ((i+1) % intvl)==0:
        
            #Ciclo que coloca los datos en sus respectivos bins
            for value in data3:
                
                cadcq = math.floor(value/bsize)
                if cadcq < tbins:
                    
                    data2[int(cadcq)] = data2[int(cadcq)] + 1
                    
                else:
                    
                    pass
                
            #Ciclo que acorta el rango que se analizara en el histograma de carga y saca el logaritmo de los eventos
            data4=[]
            data5=[]
        
            for j in range(len(data1)):
                
                if j<150:
                    
                    pass
                
                elif j>1100:
                    
                    pass
                
                else:
                    
                    try:
                        
                        data4.append(data1[j])
                        data5.append(np.log10(data2[j]))
                        
                    except:
                        
                        data4.append(data1[j])
                        data5.append(0)
        
            #Funcion que describe una parte del histograma de carga
            func1=np.polyfit(data4,data5,4)
            func1=np.poly1d(func1)
            
            #Ciclos que analizan la "rodilla" de la funcion dada
            
            #Calculo de la primera derivada
            drvt1=[]
            
            for j in range(len(data4)):
                
                drvt1.append(derivative(func1, data4[j], dx=10**(-10),n=1))
            
            func2=np.polyfit(data4,drvt1,4)
            func2=np.poly1d(func2)
            
            #Calculo de la segunda derivada
            drvt2=[]
            
            for k in range(len(data4)):
                
                drvt2.append(10**(6)*derivative(func2,data4[k],dx=10**(-10),n=1))
            
            func3=np.polyfit(data4,drvt2,4)
            func3=np.poly1d(func3)

            #Encontrar los puntos de inflexión dados por los mínimos absolutos de la segunda derivada            
            
            chrg2=0
            chrg3=0
            mini1=10000
            mini2=10000
            
            for l in range(len(data4)):
                
                if abs(func3(data4[l]))<mini1 and (abs(data4[l]-chrg3)>50):
                    
                    mini1=abs(func3(data4[l]))
                    chrg2=data4[l]
                
                elif (abs(func3(data4[l]))<mini2) and (data4[l]!=chrg2) and (abs(data4[l]-chrg2)>50):
                    
                    mini2=abs(func3(data4[l]))
                    chrg3=data4[l]
                
                else:
                    pass
            
            #Orden de las cargas de acuerdo a tamaño y calculo de los limites de la banda muonica            
            
            if chrg2>chrg3:
                
                chrg4=chrg2
                chrg2=chrg3
                chrg3=chrg4
                chrg4=int(math.floor(((chrg2+chrg3)/2)*0.9*(1+(2*derad/dehei)**2)**0.5))
                
            else:
                
                chrg4=int(math.floor(((chrg2+chrg3)/2)*0.9*(1+(2*derad/dehei)**2)**0.5))
            
            #Suma de los eventos muónicos            
            
            tsum1=0
            
            for m in range(chrg4-chrg2+1):
                
                tsum1=tsum1+10**func1(chrg2+m)
            
            #Añadir los resultados a las listas respectivas            
            
            data6.append(int(math.floor(((chrg3+chrg2)/2))))
            data7.append(int(math.floor(10**(func1((chrg3+chrg2)/2)))))
            data8.append(int(math.floor(tsum1)))
            
            #Graficas de procedimiento
            figure()
            rc("font", size=10)
            subplot(2,2,1)
            plot(data1,data2)
            title("Carga y conteo de eventos", )
            xlabel("carga [ADCq]")
            ylabel("No. de eventos")
            tight_layout()
            subplot(2,2,2)           
            plot(data1,np.log10(data2).tolist())
            plot(data4,func1(data4).tolist(),linewidth=3)
            plot(data6[-1],np.log10(data7[-1]),"o")
            plot((chrg2,chrg2), (0, func1(chrg2)), "-k")
            plot((chrg4,chrg4), (0, func1(chrg4)), "-k")
            title("Carga y conteo de eventos")
            xlabel("carga [ADCq]")
            ylabel("Logaritmo base 10 de No. de eventos")
            tight_layout()
            subplot(2,2,3)
            plot(data4,func2(data4))
            plot(data6[-1],func2(data6[-1]),"ro")
            title("Primera derivada")
            tight_layout()
            subplot(2,2,4)
            plot(data4,func3(data4)/10**(6))
            plot(data6[-1],func3(data6[-1])/10**(6),"ro")
            title("Segunda derivada")
            tight_layout()
            
            #Limpieza de lista de almacenamiento de datos
            data3=[]
            data2 = np.zeros((tbins)).tolist()

        else:
                
            pass
    
        #Añadir una hora al contador
        cdate=cdate+timedelta(0,3600)
    
        #Progreso
        print(str(i+1)+"/"+str(dhour)+" = "+str(round(float(i+1)/float(dhour),2)*100)+" %")
    
    except:
        
        #Avisar acerca del error
        
        data6.append("Error")
        data7.append("-")
        data8.append("-")
        
        #Añadir una hora al contador
        cdate=cdate+timedelta(0,3600)
    
        #Progreso
        print(str(i+1)+"/"+str(dhour)+" = "+str(round(float(i+1)/float(dhour),2)*100)+" %")       

#Guardar datos en un archivo de texto

#----------------------------------------------------------------------------------------------------------# 
          
rtext = open(str(rfnam)+".txt", "w")

for n in range(len(data6)):
    if n==0:
        rtext.write(str(data6[n])+"    "+str(data7[n])+"    "+str(data8[n]))
    else:
        rtext.write("\n"+str(data6[n])+"    "+str(data7[n])+"   "+str(data8[n]))

rtext.close()

#Fin del programa
print("\n")
print(datetime.now())