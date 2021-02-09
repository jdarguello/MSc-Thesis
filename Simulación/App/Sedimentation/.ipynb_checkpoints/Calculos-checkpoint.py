from math import sqrt, pi, cos, tan, sin
from IPython.display import Markdown, display

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

class Lamela():
    """
        Objetivo: dimensionamiento de una sola lamela
    """
    def __init__(self, fluido, prop, geo, velRes, N=1):
        Lb = geo['Longitud lamela [cm]']/geo['Ancho lamela [cm]']   #Relación largo-acho de la lamela
        #Caudal total
        Q = (fluido["Volumen [L]"]/1000)/(fluido['Tiempo objetivo [h]']*3600) #m3/s
        W = self.W(Q/N, Lb, geo['Inclinación [°]'], geo['Ancho lamela [cm]']/100, velRes['U'])
        print("W_i", W)
        Al = W*geo['Ancho lamela [cm]']/100    #Área de entrada a la lamela
        #Velocidad fluido en lamela
        v0 = self.V0(Q/N, geo['Inclinación [°]'], Al)
        print("v0", v0)
        #Reynolds
        Re = self.Re(v0, geo['Ancho lamela [cm]']/100, prop['visc'])
        print("Re", Re)
        """
        if Re > 500:
            Re = 500
            #---Recalcular variables---
            v0 = self.RV0(Re, geo['Ancho lamela [cm]']/100, prop['visc'])
            Al = self.RA(v0, Q/N, geo['Inclinación [°]'])
            W = Al/geo['Ancho lamela [cm]']/100
            U = self.RU(Q/N, Lb, geo['Inclinación [°]'], geo['Ancho lamela [cm]']/100, W)
            print("W", W)
            print("U",U)
        """
        #Número de lamelas
        Lc = self.Lc(Lb, Re)
        Nl = self.N(Lc, geo['Inclinación [°]'], geo['Ancho lamela [cm]']/100, geo['Distancia entre lamelas [cm]']/100)
        print("Nl", Nl)
    
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
    
    def W(self, Ql, Lb, theta, b, U):
        return Ql/((Lb+tan(theta*pi/180))*b*U*cos(theta*pi/180))
    
    def Lc(self, ld, Re):
        lc = ld-0.013*Re
        if lc > 0:
            return lc
        else:
            return 0.5*ld
        
        