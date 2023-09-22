import cv2 as cv
import imutils
import numpy as np
from Intersecciones import *
from control_puntos import *

wi,hi,w,h = 120,30, 870,520 #SE ESECIFICA EL TAMAÑO DE LA VENTANA
intersecciones = Intersecciones(wi,hi,w,h)
control = Control(w,h)

dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)


# vid = cv.VideoCapture(0)
arucos = {}
arucos_esquinas={}
count = 0


def correcion(position, puntos):
    if position is not None:
        for i in puntos :
            if((position[0] + 80 >= puntos[i][0] and position[0] - 80 <= puntos[i][0]) and (position[1] + 80 >= puntos[i][1] and position[1] - 80 <= puntos[i][1])):
                return( puntos[i])
      

while (1):#27 esc; ord('s')
    # ret, frame = vid.read()
    frame = cv.imread('foto.jpg')
    frame = imutils.resize(frame,width=720)
    parameters = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(dictionary, parameters)
    
    # if (ALGO):
    EsquinasMarcadores, IdMarcadores, _ = detector.detectMarkers(frame) # _ Candidatos rechazados
    
    if IdMarcadores is not None:
        for i, esquina in zip(IdMarcadores, EsquinasMarcadores): #          0       1   2       3 (clock wise)
            # print("ID: {} Esquinas: {}; ".format(i,esquina))   #Se imprimen 1(SupIzq) - 2 - 3 - 4(InfIzq) las esquinas
            
            # Marcar Centro e ID del aruco
            centro=[int(((esquina[0][2][0]-esquina[0][0][0])/2)+esquina[0][0][0]), int(((esquina[0][2][1]-esquina[0][0][1])/2)+esquina[0][0][1])]
            frame = cv.putText(frame, f"c({centro[0]},{centro[1]})", (centro[0],centro[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0),1)
            frame = cv.putText(frame, f"{i}", (int(esquina[0][0][0]), int(esquina[0][0][1])), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),1)
            
            # Agregar arucos a un diccionario
            if i.size > 0:
                arucos[i[0]] = centro #; print(arucos)
                arucos_esquinas[i[0]] = esquina
  
        # Dibujar bordes del aruco
        frame = cv.aruco.drawDetectedMarkers(frame, EsquinasMarcadores, borderColor = (0,255,0))
########################################################################################################
    puntos = intersecciones.puntos(frame) #DICCIONARIO DE PUNTOS 

            ### VERTICAL ###
    # estacion = puntos.get((0,0),[0, 0]) 
    # estacion = puntos.get((1,0),[0, 0]) 
    # estacion = puntos.get((2,0),[0, 0])
    # estacion = puntos.get((3,0),[0, 0]) 
    # estacion = puntos.get((4,0),[0, 0])
    # estacion = puntos.get((5,0),[0, 0]) 
    estacion = puntos.get((0,5),[0, 0]) 
    # estacion = puntos.get((1,5),[0, 0])
    # estacion = puntos.get((2,5),[0, 0]) 
    # estacion = puntos.get((3,5),[0, 0]) 
    # estacion = puntos.get((4,5),[0, 0]) 
    # estacion = puntos.get((5,5),[0, 0])


            ### HORIZONTAL ###
    # estacion = puntos.get((0,1),[0, 0]) 
    # estacion = puntos.get((0,2),[0, 0])
    # estacion = puntos.get((0,3),[0, 0])  
    # estacion = puntos.get((0,4),[0, 0])
    # estacion = puntos.get((5,1),[0, 0])
    # estacion = puntos.get((5,2),[0, 0]) 
    # estacion = puntos.get((5,3),[0, 0])
    # estacion = puntos.get((5,4),[0, 0])
    # print(estacion)

    arucos_lista=[]
    # PUNTOS DE SIMULACION
    carro_1 = arucos.get(1) 
    carro_2 = arucos.get(2)
    carro_3 = arucos.get(3)
    carro_4 = arucos.get(4)

    lista1 = correcion(carro_1, puntos)
    lista2 = correcion(carro_2, puntos)
    lista3 = correcion(carro_3, puntos)
    lista4 = correcion(carro_4, puntos)
    
    if lista1 is not None: arucos_lista.append(lista1)
    if lista2 is not None: arucos_lista.append(lista2)
    if lista3 is not None: arucos_lista.append(lista3)
    if lista4 is not None: arucos_lista.append(lista4)

    if arucos_lista is not None:
        coordenadas,ordenes = intersecciones.Cercano(arucos_lista,estacion) #intersecciones es lo que se manda al robot
        # print(coordenadas)

        

        esquinas_C1 =  [[(coordenadas[0]-8),(coordenadas[1]-8)],
                        [(coordenadas[0]+8),(coordenadas[1]-8)],
                        [(coordenadas[0]+8),(coordenadas[1]+8)],
                        [(coordenadas[0]-8),(coordenadas[1]+8)],]

        # #######################ORIENTACION Y MOVIMIENTO###################################
        # if (esquinas_C1[0][0]-estacion[0]<=0): direccion_x = 'x'
        # else: direccion_x = '-x'
        # if (esquinas_C1[0][1]-estacion[1]<=0): direccion_y = 'y'
        # else: direccion_y = '-y'

        # ##PRIMERO SABER PARA DONDE DEBE MIRAR EL CARRO###
        if (estacion[1]==puntos.get((0,0))[1]) or (estacion[1]==puntos.get((0,5))[1]) : #Entra en VERTICAL primero me muevo en x
        #     if esquinas_C1[0][0]+8-estacion[0]<0 :mirar="derecha" #La diferencia entre el centro y la estación
        #     elif esquinas_C1[0][0]+8-estacion[0]>0 :mirar="izquierda"
        #     else: mirar=0

        #     if count>=1:
        #         # print(mirar)
        #         esquinas_C1 = control.Giro(esquinas_C1,control.mirar(esquinas_C1,mirar))
        #     if count>=2:
        #         esquinas_C1 = control.avanza(esquinas_C1,ordenes[0],direccion_x)

        #     if count>=3:
        #         if esquinas_C1[0][0]+8==estacion[0] and esquinas_C1[0][1]+8==estacion[1]: #si ya llegó al punto pero no esta orientado
        #             if (estacion[1]==puntos.get((0,0))[1]): mirar="arriba"
        #             else: mirar="abajo"
        #         elif esquinas_C1[0][1]+8-estacion[1]>0 :mirar="arriba"
        #         elif esquinas_C1[0][1]+8-estacion[1]<0 :mirar="abajo"
        #         else: mirar=0
        #         esquinas_C1 = control.Giro(esquinas_C1,control.mirar(esquinas_C1,mirar))

        #     if count>=4:
        #         esquinas_C1 = control.avanza(esquinas_C1,ordenes[1],direccion_y)

            cv.line(frame, coordenadas, (estacion[0], coordenadas[1]), (0,255,255), 2) # LINEA Horizontal
            cv.line(frame, estacion, (estacion[0], coordenadas[1]), (0,255,255), 2)    # LINEA Vertical
            
        else:#######################################################################################
        #     if esquinas_C1[0][1]+8-estacion[1]>0 :mirar="arriba"
        #     elif esquinas_C1[0][1]+8-estacion[1]<0 :mirar="abajo"
        #     else:mirar=0
        #     if count>=1:
        #         esquinas_C1 = control.Giro(esquinas_C1,control.mirar(esquinas_C1,mirar))
        #     if count>=2:
        #         esquinas_C1 = control.avanza(esquinas_C1,ordenes[1],direccion_y)

        #     if count>=3:
        #         if esquinas_C1[0][0]+8==estacion[0] and esquinas_C1[0][1]+8==estacion[1]:
        #             if (estacion[0]==puntos.get((0,1))[0]):mirar="izquierda"
        #             else: mirar="derecha"
        #         elif esquinas_C1[0][0]+8-estacion[0]<0 :mirar="derecha"
        #         elif esquinas_C1[0][0]+8-estacion[0]>0 :mirar="izquierda"
        #         else: mirar=0
        #         esquinas_C1 = control.Giro(esquinas_C1,control.mirar(esquinas_C1,mirar))

        #     if count>=4:
        #         esquinas_C1 = control.avanza(esquinas_C1,ordenes[0],direccion_x)

            cv.line(frame, coordenadas, (coordenadas[0], estacion[1]), (0,255,255), 2) # LINEA Horizontal
            cv.line(frame, estacion, (coordenadas[0], estacion[1]), (0,255,255), 2)    # LINEA Vertical

        # cv.line(frame, esquinas_C1[0], esquinas_C1[1], (255,0,0), 1) #Frontal
        # cv.line(frame, esquinas_C1[3], esquinas_C1[2], (0,255,0), 1) 
        # cv.line(frame, esquinas_C1[0], esquinas_C1[3], (0,255,0), 1) 
        # cv.line(frame, esquinas_C1[1], esquinas_C1[2], (0,255,0), 1) 
        # # cv.putText(frame, ".", (esquinas_C1[0][0]-3,esquinas_C1[0][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)

    ###############ESTO ES PARA LOS CARROS#################
    cv.putText(frame, ".", (estacion[0]-3,estacion[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),3)
    # cv.putText(frame, ".", (carro_1[0]-3,carro_1[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),3) ;cv.putText(frame, "1", (carro_1[0]+10,carro_1[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)
    # cv.putText(frame, ".", (carro_2[0]-3,carro_2[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),3) ;cv.putText(frame, "2", (carro_2[0]+5,carro_2[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)
    # cv.putText(frame, ".", (carro_3[0]-3,carro_3[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),3) ;cv.putText(frame, "3", (carro_3[0]+5,carro_3[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)
    # cv.putText(frame, ".", (carro_4[0]-3,carro_4[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),3) ;cv.putText(frame, "4", (carro_4[0]+5,carro_4[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)


    if cv.waitKey(1) & 0xFF == 13:
        if count<=3:count += 1
        else: count=0
        if count==1 or count==3: print("{0}:Orientando...".format(count))
        elif count==2 or count==4: print("{0}:Desplazando...".format(count))

    if cv.waitKey(1) & 0xFF == 27:
      break

    cv.imshow('webCam',frame)

# vid.release()
cv.destroyAllWindows()