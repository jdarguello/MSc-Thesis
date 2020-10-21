from IPython.display import display, Markdown
from math import cos, sin, radians

def TablaResumen(lamela, res_oper, res_sed, Hazen):
    tabla = """| Propiedad | Valor |
|---|---|
| Caudal sistema $[cm^3/s ]$ | QT |
| Vel. flujo lamela $[cm / min]$ | VLAM |
| Número Reynolds | RE |
| Vel. sedimentación $[cm/min]$ | VSED |
| Eficiencia $[\%]$ | EF |
| Tiempo sed. $[s]$ | TSED |
        """
    
    tabla = tabla.replace("QT", str(round(lamela['Q_T']*1000*1000,2)))
    tabla = tabla.replace("VLAM", str(round(lamela['V_L']*100*60,2)))
    tabla = tabla.replace("RE", str(round(res_oper['Re'],2)))
    tabla = tabla.replace("VSED", str(round(res_sed['V_sed']*100*60,2)))
    tabla = tabla.replace("EF", str(round(res_sed['Ef']*100,2)))
    tabla = tabla.replace("TSED", str(round(Hazen['t_sed'],2)))
    
    display(Markdown(tabla))

class Resul():
    def __init__ (self, prop, V_sc, solid):
        #V = self.Vsed(solid['Densidad media [kg/m3]']/10**(9), prop['rho']/10**(9), solid['Tamaño de partícula medio [um]']/(10**6)*100, prop['visc']*10**6)
        V = self.Vs(prop['S_s'], prop['visc'])
        Ef = self.Eficiencia(V_sc, V)
        
        self.resul = {
            'V_sed': V, 
            'Ef': Ef
        }
        
        self.Impresion()
    
    def Impresion(self):
        msg = "La velocidad de sedimentación de las partículas es de $V_{sed} = VSED [cm/s]$. La _eficiencia_ del sistema de filtrado es del $EFI \%$."
        
        msg = msg.replace("VSED", str(round(self.resul['V_sed']*100, 3)))
        msg = msg.replace("EFI", str(round(self.resul['Ef']*100, 3)))
        
        
        display(Markdown(msg))
    
    def __call__(self):
        return self.resul
    
    def Vs(self, Ss, mu, g=9.81, x = 0.71):
        return x*(g*(Ss-1)*mu)**(1/3)
        
    def Vsed(self, rho_sol, rho_liq, d_part, mu, g=9.81):
        return 0.22*(((g*((rho_sol-rho_liq)/rho_liq))**(2/3)))*(d_part/((mu/rho_liq)**(1/3)))

    def Eficiencia(self, V_sc, V0):
        return 1-V_sc/V0

class Tiempo():
    def __init__(self, e, theta, V_sed):
        H = self.HSed(e, theta)
        t_sed = self.time(H/100, V_sed)
        
        self.resul = {
            'H_sed':H, 
            't_sed': t_sed
        }
        
        self.Impresion()
    
    def __call__(self):
        return self.resul
    
    def Impresion(self):
        msg = "La altura de sedimentación tiene un valor de $H_{sed} = HSED [cm]$. Es debido a ello que el tiempo de sedimentación es de $t_{sed} = TSED [s]$."
        
        msg = msg.replace("HSED", str(round(self.resul['H_sed'], 2)))
        msg = msg.replace("TSED", str(round(self.resul['t_sed'],2)))
         
        display(Markdown(msg))
    
    def time(self, H, V_sed):
        return H/V_sed
    
    def HSed(self, e, theta):
        return e/cos(radians(theta))
        