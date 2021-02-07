class Romero():
    """
        Objetivo: desarrollar los cálculos teóricos
    """
    def __init__(self, fluido, prop):
        Q = (fluido["Volumen [L]"]/1000)/(fluido['Tiempo objetivo [h]']*3600) #m3/s
        