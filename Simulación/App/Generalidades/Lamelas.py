import ipywidgets as widgets
from math import floor
from IPython.display import display, Markdown

def Requerimientos():
    Req = widgets.Accordion(children=[widgets.FloatText(value=5),
                                      widgets.IntText(value=8),
                                      widgets.IntText(value=5),
                                      widgets.IntSlider(value=60, max=90),
                                      widgets.FloatText(value=180)])
    
    Req.set_title(0, 'Ancho lamela [cm]')
    Req.set_title(1, 'Rel. longitud - ancho')
    Req.set_title(2, 'Número de lamelas')
    Req.set_title(3, 'Inclinación [°]')
    Req.set_title(4, 'Carga superficial [m/d]')
    return Req

def Geometry():
    Req = Requerimientos()
    tab = widgets.Tab()
    tab.children = [Req]
    return tab

def Flujo_int(geo, general):
    #Caudal dentro de una lamela
    Num_lamelas = geo['Número de lamelas']
    Q_T = (general['Fluido']['Volumen [L]']/1000)/(general['Fluido']['Tiempo objetivo [h]']*3600)
    Q_L = Q_T/Num_lamelas     #m3/s
    
    #Velocidad dentro de una lamela
    Area = (geo['Altura lamela [cm]']/100)*(geo['Ancho lamela [cm]']/100)
    Vel = Q_L/Area   #m/s
    
    msg = "El caudal requerido por el sistema es de $Q = QT \left[cm^3 /s \\right]$. Con base en la geometría dada, significa que la velocidad del fluido dentro de cada lamela es de $V = VEL [cm/min]$."
    msg = msg.replace("QT", str(round(Q_T*1000*1000, 3)))
    msg = msg.replace("VEL", str(round(Vel*100*60, 3)))
    display(Markdown(msg))
    
    return {'Q_L': Q_L, 'Q_T': Q_T, 'V_L': Vel, 'Num':Num_lamelas}
    