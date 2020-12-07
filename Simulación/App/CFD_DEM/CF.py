from IPython.display import display, Markdown
import os
from math import pi

class Condiciones():
    def __init__(self, Q, D, dir="OpenFOAM/", imprime= True):
        A = pi*(D/2)**2
        V = Q/A
        if imprime:
            self.imprime(V)
        self.execute(dir)
        self.boundary(dir)
        self.velocidad(V, dir)
        self.deltaT(V, dir)
    
    def deltaT(self, V, dir, sub=200, t = 2):
        archivo = dir + "system/controlDict"
        with open(archivo, 'r') as file:
            lineas = file.readlines()
        info = ""
        delta = False
        for linea in lineas:
            palabras = linea.split(" ")
            frase = ""
            for palabra in palabras:
                if palabra == "deltaT":
                    delta = True
                if delta:
                    try:
                        float(palabra.replace(";", ""))
                        palabra = str(t/sub) + ";"
                        delta = False
                    except:
                        pass
                frase += palabra + ' '
            info += frase.replace("\n", "")[:-1] + "\n"
        
        
        with open(archivo, 'w') as file:
            file.write(info)        
    
    def velocidad(self, V, dir):
        archivo = dir + "0/U_ref"
        with open(archivo, 'r') as file:
            lineas = file.readlines()
        ya = False
        info = ""
        #print(lineas)
        for linea in lineas:
            if linea == '    ingreso\n':
                ya = True
            elif linea == '    salida\n':
                ya = False
            if ya:
                linea = linea.replace("VV", str(V))
            info += linea
        with open(dir + "0/U", "w") as file:
            file.write(info)
    
    def boundary(self, dir):
        archivo = dir + "constant/polyMesh/boundary"
        with open(archivo, 'r') as file:
            lineas = file.readlines()
        dic = {
            'back\n':[False, "empty"],
            'front\n':[False, "empty"],
            'defaultFaces\n': [False, "wall"]
        }
        info = ""
        for linea in lineas:
            #líneas a poner
            poner = True
            #print(linea.split(" "))
            for palabra in linea.split(" "):
                if palabra == "physicalType":
                    poner = False
                #definición de condiciones 'wall', 'inlet' y 'outlet'
                for cond in dic:
                    if cond == palabra:
                        dic[cond][0] = True
                        key = cond
                    if dic[cond][0] and palabra == "type":
                        dic[key][0] = False
                        linea = linea.replace("patch", dic[cond][1])
            if poner:
                info += linea
        with open(archivo, "w") as file:
            file.write(info)
    
    def execute(self, dir):
        os.chdir("OpenFOAM")
        os.system("gmshToFoam " + "geometria.msh")
        os.chdir("..")
    
    def imprime(self, V):
        msg = """|__Zona__|__Propiedad__|__Valor__|__Tipo__|
|--------|-------------|--------|-----------|
|_Entrada_| Velocidad $[cm/h]$ |VEL |Neumann|
|_Salida_ | Presión $[KPa]$    | PRE| Dirichlet|
        """
        msg = msg.replace("VEL", str(round(V*100, 3)))
        msg = msg.replace("PRE", str(101.325))
        display(Markdown(msg))
        