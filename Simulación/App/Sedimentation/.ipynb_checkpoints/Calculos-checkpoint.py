from math import sqrt, pi, cos, tan, sin
from IPython.display import Markdown, display
try:
    from App.Sedimentation.Area import Geometria
except:
    from .Area import Geometria


class VelCr():
    #Objetivo: calcular la velocidad crítica de sedimentación
    def __init__(self, lamela, geo):
        Uc = self.Uc(lamela['v0'], geo['Inclinación [°]'], geo['Rel. longitud - ancho'])
        self.imprime(Uc)
    
    def imprime(self, Uc):
        msg = "La velocidad crítica de asentamiento tiene un valor de $" + str(round(Uc*100, 3)) + " [cm/s]$."
        
        display(Markdown(msg))
        
    def Uc(self, v0, theta, Lb):
        return v0/(sin(theta*pi/180)+Lb*cos(theta*pi/180))

    
class VelSed():
    """
        Calcula el valor de la velocidad de sedimentación. 
        Para ello, se realiza un proceso iterativo suponiendo una velocidad de asentamiento, recalculando y comparándola.
    """
    def __init__(self, solid, fluido):
        U_s = 0
        U_c = 1
        error = 1
        while error > 0.0001:
            U_s = U_c
            Res = self.Reynolds(U_s, solid['Tamaño de partícula medio [um]']/1000000, fluido['visc'])
            C = self.C(Res)
            U_c = self.U(solid['Tamaño de partícula medio [um]']/1000000, solid['Densidad media [kg/m3]'], fluido['rho'], C)
            error = (U_s-U_c)/U_s
        self.res = {
            'U': U_c,    #m/s
            'Res': Res,
            'C':C
        }
        self.imprime()
    
    def imprime(self):
        msg = """El proceso iterativo, con una estimación de error del $0.01 \%$, arroja los siguientes resultados: $U = VSED [m/s]$ y un número de Reynolds de $Re_s = RES$. """
        
        msg = msg.replace("VSED", str(round(self.res['U'], 3)))
        msg = msg.replace("RES", str(round(self.res['Res'],3)))
        display(Markdown(msg))
    
    def U(self, dp, rho_s, rho_f, C):
        g = 9.81
        V = (4/3)*pi*(dp/2)**3
        A_n = pi*(dp/2)**2
        return sqrt((2*V*(rho_s-rho_f)*g)/(C*A_n*rho_f))
    
    def C(self, Re):
        return (24/Re)+(3/(Re**(1/2)))+0.34
    
    def Reynolds(self, U, dp, mu):
        return (dp*U)/mu
    
    def __call__(self):
        return self.res

class Lamela(Geometria):
    """
        Objetivo: dimensionamiento de una sola lamela
    """
    def __init__(self, fluido, prop, geo, velRes):
        L = geo['Ancho lamela [cm]']*geo['Rel. longitud - ancho']/100    #Longitud de una lamela - m
        #Caudal total
        Q = (fluido["Volumen [L]"]/1000)/(fluido['Tiempo objetivo [h]']*3600) #m3/s
        
        #super().__init__(Q, geo['Longitud lamela [cm]']/100, geo['Ancho lamela [cm]']/100, geo['Inclinación [°]'], prop['nu'])
        CS = geo['Carga superficial [m/d]']/24/3600
        #CS = velRes['U']
        W = self.W(CS, Q, geo['Número de lamelas'], geo['Rel. longitud - ancho'], geo['Inclinación [°]'], geo['Ancho lamela [cm]']/100)
        Al = W*geo['Ancho lamela [cm]']/100    #Área de entrada a la lamela
        #Velocidad fluido en lamela
        v0 = Q/(geo['Número de lamelas']*geo['Ancho lamela [cm]']/100*W)
        #Reynolds
        Re = self.Re(v0, geo['Ancho lamela [cm]']/100, prop['visc'])
        
        self.res = {
            'QT':Q, 
            'ancho': W,
            'v0': v0,
            "Reynolds": Re
        }
        
        self.imprime()
    
    def __call__(self):
        return self.res
    
    def imprime(self):
        msg = """| Propiedad | Valor |
|---|---|
| $Q \, [L / min ]$ | QT |
| $W \, [m]$|ancho|
|$v_0 \, [cm / s]$|v0|
| $Re$ | Reynolds |
        """
        mult = 1
        for key in self.res:
            if key == 'QT':
                mult = 1000*60
            elif key == 'v0':
                mult = 100
            else:
                mult = 1
            msg = msg.replace(key, str(round(self.res[key]*mult,3)))
            
        display(Markdown(msg))
        

    def CS(self, Q, N, L, b, theta, W):
        return Q/(N*((L/b)+tan(theta*pi/180))*b*W*cos(theta*pi/180))

    def RU(self, Ql, Lb, theta, b, W):
        return Ql/((Lb+tan(theta*pi/180))*b*W*cos(theta*pi/180))
    
    def RA(self, v0, Ql, theta):
        return Ql/(v0*sin(theta*pi/180))
    
    def RV0(self, Re, d, mu):
        return Re*mu/d
        
    def N(self, Lc, theta, d, e):
        return (Lc*sin(theta*pi/180))/(d+e)
    
    def Re(self, v0, d, mu):
        return v0*d/mu
    
    def V0(self, Ql, theta, Al):
        return Ql/(Al*sin(theta*pi/180))
    
    def W(self, U, Q, N, Lb, theta, b):
        return Q/(N*(Lb+tan(theta*pi/180))*b*U*cos(theta*pi/180))
    
    def Lc(self, ld, Re):
        lc = ld-0.013*Re
        if lc > 0:
            return lc
        else:
            return 0.5*ld
        
        