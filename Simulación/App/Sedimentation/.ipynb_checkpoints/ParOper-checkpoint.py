from math import sin, cos, radians
from IPython.display import Markdown, display

class Parametros():
    resul = {}
    def __init__(self, general, prop, lamela, geo):
        
        L_rel = (geo['Altura panel [cm]']/sin(radians(geo['Inclinación [°]'])))/geo['Ancho lamela [cm]']
        V = self.Vsc(lamela['V_L'], geo['Inclinación [°]'], L_rel)
        
        Rh = self.Rh(geo['Ancho lamela [cm]']/100, geo['Largo panel [cm]']/100)
        Re = self.Reynolds(lamela['V_L'], Rh, prop['visc'])
        
        self.resul = {
            'L_rel': L_rel,
            'V': V,
            'Rh': Rh,
            'Re': Re
        }
        
        self.Imprime(lamela['V_L'])
        
    def Imprime(self, VL):
        msg = "El valor de sedimentación crítica, de acuerdo a la _fórmula de Yao_, es de $V_{sc} = VSC \cdot 10^{-3} [cm/s]$. A la velocidad de flujo dada, se tiene un número de Reynolds de $Re = RE$, "
        
        msg = msg.replace('RE', str(round(self.resul['Re'], 3)))
        msg = msg.replace('VSC', str(round(self.resul['V']*1000, 3)))
        
        if self.resul['Re'] < 250:
            msg += "garantizando un flujo laminar en dentro de las lamelas."
        else:
            msg += "lo que significa que se presentan _turbulencias_ dentro de los paneles."
        
        display(Markdown(msg))
            
    def __call__(self):
        return self.resul
    
    def Reynolds(self, V0, Rh, mu):
        return (4*V0*Rh)/(mu)
        
    def Rh(self, b, e):
        return (b*e)/(2*(b+e))
    
    def Vsc(self, V0, theta, L_rel):
        return V0/(sin(radians(theta)) + L_rel*cos(radians(theta)))    