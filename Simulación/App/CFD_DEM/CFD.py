import subprocess
import os

class FOAM():
    def __init__(self):
        raw = self.fire()
        self.imprime(raw)
        self.view()
    
    def view(self):
        p = subprocess.run("paraFoam", cwd="OpenFOAM")
    
    def imprime(self, raw):
        def decompose(info):
            bites = raw[0].split(b'\n')
            for linea in bites:
                frase = ''
                for palabra in linea.decode("utf-8"):
                    frase += palabra
                print(frase)
        decompose(raw[0])
    
    def fire(self):
        os.chdir("OpenFOAM")
        #os.system("icoFoam")
        p = subprocess.Popen(["icoFoam"], stdout=subprocess.PIPE, shell=True)
        p.wait()
        os.chdir("..")
        (output, err) = p.communicate()
        return output, err
        