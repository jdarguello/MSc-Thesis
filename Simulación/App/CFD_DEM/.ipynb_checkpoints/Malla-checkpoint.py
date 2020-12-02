import subprocess
import os
from IPython.display import display, Markdown

class ToFoam():
    def __init__(self, file="./OpenFOAM/geometria.msh"):
        raw = self.bash(file)
        out = self.evaluacion(raw)
        try:
            self.imprime(out)
        except:
            pass
    
    def evaluacion(self, raw):
        bites = raw.split(b'\n')
        data = {}
        fin = False
        for linea in bites:
            frase = ''
            for palabra in linea.decode("utf-8"):
                frase += palabra
            print(frase)
            cont = 0
            palabras = frase.split()
            for i in range(len(palabras)):
                if fin and palabras[i] == "Mesh":
                    data[palabras[i]] = palabras[i+1]
                    fin = False
                    break
                if not fin:
                    for par in (("Max", "Max aspect ratio"), ("Non-orthogonality", "Non-orthogonality check"), ("Max", "Max skewness")):
                        try:
                            if par[0] == palabras[i] and palabras[i] + ' ' + palabras[i+1] ==par[1]:
                                if par[1] == "Max skewness":
                                    fin = True
                                if palabras[i+2] != "=":
                                    sumando = 2
                                else:
                                    sumando = 3
                                resul = ""
                                for valor in palabras[i+sumando:]:
                                    resul += valor
                                    resul += " "
                                data[par[1]] = resul
                            if par[0] == palabras[i] and palabras[i] + ' ' + palabras[i+1] + ' ' + palabras[i+2] ==par[1]:
                                data[par[1]] = palabras[i+4]
                        except:
                            break
        return data
    
    def imprime(self, out):
        msg = """|__Parámetro__|__Valor__|
|--------|-------------|
|Apertura _máxima_ entre elementos| APEREL|
|Checkeo de _no_ ortogonalidad|CHCK|
|Oblicuidad máxima|SKEW|
|Conclusión de malla|RES|
        """
        
        msg = msg.replace("APEREL",  out['Max aspect ratio'])
        msg = msg.replace("CHCK", out['Non-orthogonality check'])
        msg = msg.replace("SKEW", out['Max skewness'])
        msg = msg.replace("RES", out['Mesh'])
        
        display(Markdown(msg))
        
    def bash(self, file):
        root =  os.getcwd() + '/'
        os.system("gmshToFoam " + file)
        p = subprocess.Popen(["checkMesh"], stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        return output
        