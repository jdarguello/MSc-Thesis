from IPython.display import display, Markdown

class Condiciones():
    def __init__(self, V):
        self.imprime(V)
    
    def imprime(self, V):
        msg = """|__Zona__|__Propiedad__|__Valor__|__Tipo__|
|--------|-------------|--------|-----------|
|_Entrada_| Velocidad $[cm/h]$ |VEL |Neumann|
|_Salida_ | Presión $[KPa]$    | PRE| Dirichlet|
        """
        msg = msg.replace("VEL", str(round(V*100, 3)))
        msg = msg.replace("PRE", str(101.325))
        display(Markdown(msg))
        