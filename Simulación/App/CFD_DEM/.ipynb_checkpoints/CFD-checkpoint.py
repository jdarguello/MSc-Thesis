import subprocess
import os
import shutil as sh
from IPython.display import Markdown, display

def clean(dir="OpenFOAM"):
    clasicas = ("0", "constant", "system", "geometria.msh")
    for file in os.listdir(dir):
        delete = True
        for carpeta in clasicas:
            if carpeta == file:
                delete = False
        if delete:
            d = dir + '/' + file
            try:
                os.remove(d)
            except:
                sh.rmtree(d)

class FOAM():
    def __init__(self, folder="OpenFOAM", solver="icoFoam"):       
        clean()
        raw = self.fire(folder, solver)
        self.imprime(raw)
        self.view()
    
    def view(self):
        p = subprocess.run("paraFoam", cwd="OpenFOAM")
    
    def imprime(self, raw):
        display(Markdown("__Información en crudo:__"))
        def decompose(info):
            bites = raw[0].split(b'\n')
            for linea in bites:
                frase = ''
                for palabra in linea.decode("utf-8"):
                    frase += palabra
                print(frase)
        decompose(raw[0])
    
    def fire(self, folder, solver):
        os.chdir(folder)
        #os.system("icoFoam")
        p = subprocess.Popen([solver], stdout=subprocess.PIPE, shell=True)
        os.chdir("..")
        (output, err) = p.communicate()
        return output, err
        