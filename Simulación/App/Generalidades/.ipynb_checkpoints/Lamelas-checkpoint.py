import ipywidgets as widgets
from math import floor
from IPython.display import display, Markdown

def Requerimientos():
    Req = widgets.Accordion(children=[widgets.FloatText(value=25),
                                      widgets.FloatText(value=30),
                                      widgets.FloatText(value=30),
                                      widgets.FloatText(value=2.5),
                                      widgets.IntSlider(value=60, max=90)])
    Req.set_title(0, 'Ancho panel [cm]')
    Req.set_title(1, 'Altura panel [cm]')
    Req.set_title(2, 'Largo panel [cm]')
    Req.set_title(3, 'Ancho lamela [cm]')
    Req.set_title(4, 'Inclinación [°]')
    return Req

def Geometry():
    Req = Requerimientos()
    tab = widgets.Tab()
    tab.children = [Req]
    return tab

def Flujo_int(geo, general):
    #Caudal dentro de una lamela
    Num_lamelas = floor(geo['Ancho panel [cm]']/geo['Ancho lamela [cm]'])
    Q_T = (general['Fluido']['Volumen [L]']/1000)/(general['Fluido']['Tiempo objetivo [h]']*3600)
    Q_L = Q_T/Num_lamelas     #m3/s
    
    #Velocidad dentro de una lamela
    Area = (geo['Largo panel [cm]']/100)*(geo['Ancho lamela [cm]']/100)
    Vel = Q_L/Area   #m/s
    
    msg = "El caudal requerido por el sistema es de $Q = QT \left[cm^3 /s \\right]$. Con base en la geometría dada, significa que la velocidad del fluido dentro de cada lamela es de $V = VEL [cm/min]$."
    msg = msg.replace("QT", str(round(Q_T*1000*1000, 3)))
    msg = msg.replace("VEL", str(round(Vel*100*60, 3)))
    display(Markdown(msg))
    
    return {'Q_L': Q_L, 'Q_T': Q_T, 'V_L': Vel, 'Num':Num_lamelas}
    