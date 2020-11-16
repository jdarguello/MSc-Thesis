import ipywidgets as widgets

def Read(raw, datos={'Fluido':{}, 'Solid':{}}):
    cont = 0
    for tipo in datos:
        suma = 0
        while True:
            try:
                if tipo != 'Tamaño de malla':
                    datos[tipo][raw.children[cont].get_title(suma)] = raw.children[cont].children[suma].value
                else:
                    datos[tipo] = raw.children[cont].value
                    break
                suma += 1
            except:
                break
        cont += 1
    return datos

def ReadMesh(raw):
    cont = 0 
    data = {}
    while True:
        try:
            data[raw.children[1].get_title(cont)] = raw.children[1].children[cont].value
        except:
            break
        cont += 1
    return data