import cv2 as cv
import numpy as np

class Intersecciones:
   def __init__(self,wi,hi,w,h):
      self.xi = wi
      self.yi = hi
      self.x = w
      self.y = h
  
   def puntos(self, frame):
      self.distancia_x,self.distancia_y = int((self.x - (200*2))/5), int((self.y - (20*2))/5)
      puntos = {}
      # puntos = {         # ejemplo para 640x480
      #          (0,0): [20,20], (1,0): [140,20], (2,0): [260,20], (3,0): [380,20], (4,0): [500,20], (5,0): [620,20], 
      #          (0,1): [20,108],(1 ,1): [140,108],(2,1): [260,108],(3,1): [380,108],(4,1): [500,108],(5,1): [620,108], 
      #          (0,2): [20,196],(1,2): [140,196],(2,2): [260,196],(3,2): [380,196],(4,2): [500,196],(5,2): [620,196],
      #          (0,3): [20,284],(1,3): [140,284],(2,3): [260,284],(3,3): [380,284],(4,3): [500,284],(5,3): [620,284],
      #          (0,4): [20,372],(1,4): [140,372],(2,4): [260,372],(3,4): [380,372],(4,4): [500,372],(5,4): [620,372],
      #          (0,5): [20,460],(1,5): [140,460],(2,5): [260,460],(3,5): [380,460],(4,5): [500,460],(5,5): [620,460],}
      c=-1
      for i in range(self.xi,self.x,self.distancia_x):
         f=0
         c+=1
         for j in range(self.yi,self.y,self.distancia_y):
            puntos[c,f]=[i,j]
            f+=1

      # Horizontales
      cv.line(frame, puntos.get((0,0)), puntos.get((5,0)), (0,0,255), 1) 
      cv.line(frame, puntos.get((0,1)), puntos.get((5,1)), (0,0,255), 1) 
      cv.line(frame, puntos.get((0,2)), puntos.get((5,2)), (0,0,255), 1) 
      cv.line(frame, puntos.get((0,3)), puntos.get((5,3)), (0,0,255), 1)
      cv.line(frame, puntos.get((0,4)), puntos.get((5,4)), (0,0,255), 1) 
      cv.line(frame, puntos.get((0,5)), puntos.get((5,5)), (0,0,255), 1)
      # Verticales
      cv.line(frame, puntos.get((0,0)), puntos.get((0,5)), (0,0,255), 1)
      cv.line(frame, puntos.get((1,0)), puntos.get((1,5)), (0,0,255), 1)
      cv.line(frame, puntos.get((2,0)), puntos.get((2,5)), (0,0,255), 1)
      cv.line(frame, puntos.get((3,0)), puntos.get((3,5)), (0,0,255), 1)
      cv.line(frame, puntos.get((4,0)), puntos.get((4,5)), (0,0,255), 1)
      cv.line(frame, puntos.get((5,0)), puntos.get((5,5)), (0,0,255), 1)

      return puntos

   def Cercano(self,arucos_list,estacion):
      ordenes = []
      d,x,y = [],[],[]

      for i in arucos_list:
         d.append(int(abs(estacion[0]-i[0])/self.distancia_x)+int(abs(estacion[1]-i[1])/self.distancia_y))
         x.append(int(abs(estacion[0]-i[0])/self.distancia_x))
         y.append(int(abs(estacion[1]-i[1])/self.distancia_y))

      i_mnor = 0
      menor= d[i_mnor]
      for elemento in d:
         if (elemento < menor) and (elemento != menor):
            menor = elemento
            i_mnor = d.index(menor)
         
         if elemento==menor:
            #Distancias en x
            for elemento2 in x:
                  if (elemento2<menor):  #and (elemento2 != menor)
                     menorx=elemento2
                     i_mnor=x.index(menorx)
            #Distancias en y
            for elemento3 in y:
                  if (elemento3<menor): 
                     menory=elemento3
                     i_mnor=y.index(menory)
            if (menorx<menory) : menor = menorx
            else: menor = menory

      cercano = arucos_list[i_mnor]
      ordenes = [x[i_mnor],y[i_mnor]]

      return cercano,ordenes
    