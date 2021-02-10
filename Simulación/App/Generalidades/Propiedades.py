from IPython.display import Markdown, display

class SolProp():
    prop = {
        'agua': {},
        'etanol': {}
    }
    def __init__(self, datos):
        self.prop['agua'] = self.Agua(datos['Fluido']['Temperatura [°C]'])
        self.prop['etanol'] = self.Etanol(datos['Fluido']['Temperatura [°C]'])
        self.prop['mezcla'] = self.Mezcla(datos['Fluido']['Relación agua - etanol [%]']/100, datos['Solid']['Densidad media [kg/m3]'])
        self.Imprimir(datos['Fluido']['Relación agua - etanol [%]'])
    
    def Imprimir(self, porc):
        tabla = """| Propiedad | Valor |
|---|---|
| Densidad $[kg / m^3 ]$ | RHO |
|Visc. cinemática $kg \, m/s$|VISCO|
|Visc. dinámica $m^2/s$|VISCC|
| Relación de densidades | SS |
        """
        tabla = tabla.replace("RHO", "$" + str(round(self.prop['mezcla']['rho'],2)) + "$")
        viscosidad = "$" +  str(round(self.prop['mezcla']['visc']*1000000,2)) + " \, 10 ^{-6} $"
        tabla = tabla.replace("VISCO", viscosidad)
        S_s = "$" +  str(round(self.prop['mezcla']['S_s'],2)) + "$"
        tabla = tabla.replace("SS", S_s)
        nu = "$" +  str(round(self.prop['mezcla']['nu'],6)*10000) + " \, 10 ^{-4} $"
        tabla = tabla.replace("VISCC", nu)
        titulo = """#### _Propiedades termodinámicas de la mezcla agua - etanol al XXX_
        """
        porcentaje = "$" +  str(porc) + "[\%] $"
        titulo = titulo.replace("XXX", porcentaje)
        
        display(Markdown(titulo))
        display(Markdown(tabla))
        
    def Mezcla(self, x, rho_sol):
        rho_fluid = (1-x)*self.prop['agua']['rho']+(x)*self.prop['etanol']['rho'] 
        S_s = rho_sol/rho_fluid
        return {
            'rho': rho_fluid,
            'visc': (1-x)*self.prop['agua']['visc']+(x)*self.prop['etanol']['visc'],
            'nu': (1-x)*self.prop['agua']['nu']+(x)*self.prop['etanol']['nu'],
            'S_s': S_s
        }
    
    def Agua(self, T):
        rho_agua=1.00048675E+03-2.23243162E-02*T-4.60579811E-03*T**2    #kg/m3
        visc_agua = 1.63190407E-06-3.73507082E-08*T+3.20602877E-10*T**2
        nu=1.59366659E-03-3.42276923E-05*T+2.62798502E-07*T**2
        dic = {
            'rho': rho_agua,
            'visc': visc_agua,
            'nu': nu
        }
        return dic
    
    def Etanol(self, T):
        rho_eta=8.06320738E+02-8.32481402E-01*T-5.78205398E-04*T**2
        visc_eta=2.11316694E-06-3.69955667E-08*T+2.57275555E-10*T**2
        nu=1.68059553E-03-2.94778702E-05*T+1.90387050E-07*T**2
        dic = {
            'rho': rho_eta,
            'visc': visc_eta,
            'nu': nu
        }
        return dic
    
    def __call__(self):
        return self.prop
        
    
        
        