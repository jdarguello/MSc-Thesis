from IPython.display import display, Markdown

def caudal(vol, tiempo):
    tiempo = tiempo*3600    #s
    vol = vol/1000          #m3
    return vol/tiempo

class ReyLaminar():
    def __init__(self, data, prop, Q):
        Vel = self.velocidad(data, prop)
        R = self.Reynolds(Vel, data['Solid']['Tamaño de partícula medio [um]']/10**6, prop['visc'])
        self.res = {
            'V_laminar': Vel,
            'R': R
        }
        self.Impresion(Q)
    
    def Impresion(self, Q):
        mensaje = """La velocidad laminar tiene un valor de: $V_{laminar} = VLAM [cm/s]$. El número de Reynolds tendría un valor de: $Re = REYNOLDS$ a esta velocidad de flujo. Lo anterior significa que ...
        """
        mensaje = mensaje.replace("VLAM", str(round(self.res['V_laminar']*100,3)))
        mensaje = mensaje.replace("REYNOLDS", str(round(self.res['R'],3)))
        if self.res['R'] < 1:
            mensaje = mensaje.replace("...", "la interacción _fluido - partícula_ se encuentra en __régimen laminar__.")
        elif self.res['R'] > 1 and self.res['R'] < 1000:
            mensaje = mensaje.replace("...", "la interacción _fluido - partícula_ se encuentra en __régimen de transición__.")
        else:
            mensaje = mensaje.replace("...", "la interacción _fluido - partícula_ se encuentra en __régimen turbulento__.")
        display(Markdown(mensaje))
        
        mensaje = "A las condiciones dadas, se requiere una velocidad de flujo de $V = VEL$. Valor ..."
        
    
    def velocidad(self, data, prop):
        #Datos generales
        g = 9.81  #m/s2
        v = g/18*(prop['S_s']-1)*(((data['Solid']['Tamaño de partícula medio [um]']/10**6)**2)/prop['visc'])
        return v
    
    def Reynolds(self, v, d, visc):
        return v*d/visc
    
    def __call__(self):
            return self.res
    