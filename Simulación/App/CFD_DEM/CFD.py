import subprocess

class FOAM():
    def __init__(self):
        raw = self.fire()
        self.imprime(raw)
    
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
        p = subprocess.Popen(["icoFoam"], stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        return output, err
        