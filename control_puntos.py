import numpy as np

class Control:
    def __init__(self,w,h):
        self.distancia_x,self.distancia_y = int((w - (200*2))/5), int((h - (20*2))/5)
        pass

    def Giro(self, esquinas,k):
        if k == 90 : k=-2
        if k == 180: k=-4
        if k == -90: k=2
        newesquinas = np.roll(esquinas,k)
        return newesquinas

    def avanza(self, esquinas,cuanto,direccion):
        if direccion == "x": # DESPLAZAMIENTO EN X
            newesquinas = [[esquinas[i][0]+(cuanto*self.distancia_x),esquinas[i][1]] for i in range(len(esquinas))] # List Comprehesion; Sumar todos los Y de las esquinas
        if direccion == "-x": # DESPLAZAMIENTO EN X
            newesquinas = [[esquinas[i][0]-(cuanto*self.distancia_x),esquinas[i][1]] for i in range(len(esquinas))]
        if direccion == "y": # DESPLAZAMIENTO EN Y
            newesquinas = [[esquinas[i][0],esquinas[i][1]+(cuanto*self.distancia_y)] for i in range(len(esquinas))] # List Comprehesion; Sumar todos los Y de las esquinas
        if direccion == "-y": # DESPLAZAMIENTO EN Y
            newesquinas = [[esquinas[i][0],esquinas[i][1]-(cuanto*self.distancia_y)] for i in range(len(esquinas))]
        return newesquinas

    def mirar(self,mirando,mirar):
        if (mirando[0][0]-mirando[1][0]<0 and mirando[0][1]-mirando[1][1] == 0):mirada="arriba"
        elif(mirando[0][0]-mirando[1][0]>0 and mirando[0][1]-mirando[1][1] == 0):mirada="abajo"
        elif (mirando[0][1]-mirando[1][1]<0 and mirando[0][0]-mirando[1][0] == 0):mirada="derecha"
        else: mirada="izquierda"
        if mirar==0: mirar=mirada

        lvista = ["arriba","derecha","abajo","izquierda"]

        if lvista.index(mirada) == lvista.index(mirar)+2 or lvista.index(mirada) == lvista.index(mirar)-2: giro=180
        if lvista.index(mirada) == lvista.index(mirar)+1 or  lvista.index(mirada) == lvista.index(mirar)-3: giro=-90
        if lvista.index(mirada) == lvista.index(mirar)-1 or lvista.index(mirada) == lvista.index(mirar)+3: giro=90
        if lvista.index(mirada) == lvista.index(mirar): giro=0
        return giro
