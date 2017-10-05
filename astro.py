# -*- coding: utf-8 -*-
#######################################################################################
#Christian Ramírez
#Universidad del Valle de Guatemala
#Astrofísica computacional#
##################################################################################
#Ejercicio 1
def running_average():
    cuenta =0.0
    casos=0.0
    while True:
        x=yield
        casos=casos+1
        yield (cuenta +x)/casos
        cuenta = cuenta +x
        
ra = running_average()   
for value in [7, 13, 17, 231, 12, 8, 3]:
    next(ra)
    out_str = "sent: {val:3d}, new average: {avg:6.2f}"
    print(out_str.format(val=value, avg=ra.send(value)))
#########################################################################
#Ejercicio 2
class Reloj(object):
    def __init__(self, horas, minutos, segundos):
        self.set_Reloj(horas, minutos, segundos)
    def set_Reloj(self, horas, minutos, segundos):
        if type(horas) == int and 0<= horas and horas <24:
            self._horas=horas
        else:
            raise TypeError("Las horas deben ser enteras entre 0 y 23")
        if type(minutos) == int and 0<= minutos and minutos <60:
            self.__minutos=minutos
        else:
            raise TypeError("Los minutos deben ser enteros entre 0 y 59")
        if type(segundos) == int and 0<= segundos and segundos< 60:
            self.__segundos=segundos
        else:
            raise TypeError("Los segundos deben ser enteros entre 0 y 59")

    def __str__(self):
        return"{0:02d}:{1:02d}:{2:02d}".format(self._horas,self.__minutos,self.__segundos)

    def tick(self):
        if self.__segundos== 59:
            self.__segundos = 0
            if self.__minutos == 59:
                self.__minutos = 0
                if self._horas == 23:
                    self._horas = 0
                else:
                    self._horas += 1
            else:
                self.__minutos += 1
        else:
            self.__segundos += 1
def wt():
    x=Reloj(23,59,59)
    i=0
    while i < 10:
      x.tick()
      yield x
      i=i+1
#############################################################################################################################
 

      
      
      
      



