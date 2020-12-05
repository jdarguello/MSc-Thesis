import subprocess
import os
from IPython.display import display, Markdown

class ToFoam():
    def __init__(self, file="geometria.msh"):
        raw = self.bash(file)
        out, fail, crudo = self.evaluacion(raw)
        try:
            if not fail:
                self.imprime(out)
            else:
                display(Markdown("## La __malla__ presenta _no ortogonalidad_ y __no es apta__ para el desarrollo de las simulaciones numéricas."))
                display(Markdown("__Información en crudo:__"))
                for frase in crudo:
                    print(frase)
        except:
            pass
    
    def evaluacion(self, raw):
        bites = raw.split(b'\n')
        crudo = []
        data = {}
        fin = False
        fail = False
        for linea in bites:
            frase = ''
            for palabra in linea.decode("utf-8"):
                frase += palabra
            crudo.append(frase)
            cont = 0
            palabras = frase.split()
            for i in range(len(palabras)):
                if palabras[i] == "<<Writing" or palabras[i] == "Fail":
                    fail = True
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
        return data, fail, crudo
    
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
        skew = out['Max skewness'].split()[0]
        if float(skew) > 1.0:
            display(Markdown("La oblicuidad máxima es mayor a 1.0. Se recomienda disminuir el _rango_ del tamaño entre elementos para disminuir este valor."))
        else:
            display(Markdown("La malla __es apta__ para el desarrollo de las simulaciones numéricas."))
        
    def bash(self, file):
        root =  os.getcwd() + '/'
        command = "gmshToFoam " + file
        os.chdir("OpenFOAM")
        os.system(command)
        #p = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, shell=True)
        #os.system(command)
        p = subprocess.Popen(["checkMesh"], stdout=subprocess.PIPE, shell=True)
        p.wait()
        (output, err) = p.communicate()
        os.chdir("..")
        return output
        