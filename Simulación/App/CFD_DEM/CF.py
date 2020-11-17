from IPython.display import display, Markdown
import os

class Condiciones():
    def __init__(self, V):
        self.imprime(V)
        self.execute()
        self.boundary()
        self.velocidad(V)
    
    def velocidad(self, V):
        archivo = "0/U_ref"
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
        with open("0/U", "w") as file:
            file.write(info)
    
    def boundary(self):
        archivo = "constant/polyMesh/boundary"
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
    
    def execute(self):
        os.system("gmshToFoam geometria.msh")
    
    def imprime(self, V):
        msg = """|__Zona__|__Propiedad__|__Valor__|__Tipo__|
|--------|-------------|--------|-----------|
|_Entrada_| Velocidad $[cm/h]$ |VEL |Neumann|
|_Salida_ | Presión $[KPa]$    | PRE| Dirichlet|
        """
        msg = msg.replace("VEL", str(round(V*100, 3)))
        msg = msg.replace("PRE", str(101.325))
        display(Markdown(msg))
        