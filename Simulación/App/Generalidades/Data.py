import ipywidgets as widgets

def Requerimientos():
    Req = widgets.Accordion(children=[widgets.IntSlider(value=50),
                                      widgets.FloatText(value=28),
                                      widgets.FloatText(value=1),
                                      widgets.FloatText(value=200)])
    Req.set_title(0, 'Relación agua - etanol [%]')
    Req.set_title(1, 'Temperatura [°C]')
    Req.set_title(2, 'Tiempo objetivo [h]')
    Req.set_title(3, 'Volumen [L]')
    return Req

def Esp():
    Req = widgets.Accordion(children=[widgets.FloatText(value=250),
                                      widgets.FloatText(value=1700),
                                      widgets.FloatText(value=80)])
    Req.set_title(0, 'Tamaño de partícula medio [um]')
    Req.set_title(1, 'Densidad media [kg/m3]')
    Req.set_title(2, 'Masa [kg]')
    return Req

def Datos():
    Req = Requerimientos()
    E = Esp()
    tab = widgets.Tab()
    tab.children = [Req, E]
    tab.set_title(0, 'Fluido')
    tab.set_title(1, 'Material particulado')
    return tab
