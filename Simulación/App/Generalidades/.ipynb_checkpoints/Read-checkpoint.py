import ipywidgets as widgets

def Read(raw, datos={'Fluido':{}, 'Solid':{}}):
    cont = 0
    for tipo in datos:
        suma = 0
        while True:
            try:
                if tipo != 'Malla':
                    datos[tipo][raw.children[cont].get_title(suma)] = raw.children[cont].children[suma].value
                else:
                    datos[tipo] = raw.children[cont].value
                    break
                suma += 1
            except:
                break
        cont += 1
    return datos