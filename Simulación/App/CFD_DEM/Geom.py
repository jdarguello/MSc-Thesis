import pyvista as pv
import pygmsh
import ipywidgets as widgets
from math import pi, radians, cos, sin, tan, ceil
import meshio
import os
import subprocess

def Rango(minimo=250, maximo=20000):
    rango = widgets.IntRangeSlider(
        value=[4000, 20000],
        min=minimo,
        max=maximo,
        step=1,
        description='Rango [um]:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True
    )
    radio = widgets.RadioButtons(
    options=['Estructurada', 'No estructurada'],
    value='Estructurada', 
    layout={'width': 'max-content'}, # If the items' names are long
    description='Tipo:',
    disabled=False
)
    Req = widgets.Accordion(children=[rango, radio])
    Req.set_title(0, 'Tamaño de malla')
    Req.set_title(1, 'Tipo de malla')
    return Req

def Size():
    Req = widgets.Accordion(children=[widgets.FloatText(value=25),
                                      widgets.FloatText(value=20),
                                      widgets.FloatText(value=30),
                                      widgets.FloatText(value=2.5),
                                      widgets.FloatText(value=0.5),
                                      widgets.IntText(value=10),
                                      widgets.FloatText(value=0.1),
                                      widgets.IntSlider(value=60, max=90)])
    Req.set_title(0, 'Ancho panel [cm]')
    Req.set_title(1, 'Altura panel [cm]')
    Req.set_title(2, 'Largo panel [cm]')
    Req.set_title(3, 'Ancho lamela [cm]')
    Req.set_title(4, 'Distancia entre lamelas [cm]')
    Req.set_title(5, 'Número de lamelas')
    Req.set_title(6, 'Espesor [cm]')
    Req.set_title(7, 'Inclinación [°]')
    return Req

def Entrada(D_I):
    Req = widgets.Accordion(children=[widgets.FloatText(value=D_I),
                                      widgets.FloatText(value=0.5*D_I)])
    Req.set_title(0, 'Diámetro [m]')
    Req.set_title(1, 'Longitud [m]')
    return Req

def Malla(D_I):
    Req = Rango()
    Tam = Size()
    Ent = Entrada(D_I)
    tab = widgets.Tab()
    tab.children = [Req, Tam, Ent]
    tab.set_title(0, 'Malla')
    tab.set_title(1, 'Dimensiones')
    tab.set_title(2, 'Entrada')
    
    return tab


def Dibujar(geo, lamela, rango, tipo, e, entrada, DEM=True, name ="out.vtk"):
    nom_geo = "Geometry.geo"
    XXX = geo['Altura panel [cm]']/tan(radians(geo['Inclinación [°]']))    #Horizontal panel inclinado
    long_panel = ceil(geo['Altura panel [cm]']/sin(radians(geo['Inclinación [°]']))/(rango[0]/10**4))
    with open("Referencia.geo", "r", encoding="utf-8") as file:
        contenido = ""
        ver = True
        for line in file.readlines():
            if line[0:6] == "//---G":
                ver = False
            if ver:
                for var in (("DD", entrada[0]), ("LLL", entrada[1]), ("HH", geo["Altura panel [cm]"]/100), ("ALL", geo['Ancho lamela [cm]']/100), ("XXX", XXX/100), ("YYY", geo['Altura panel [cm]']/100), ("malMax", rango[1]/10**6), ("REF", long_panel), ("ESP", geo['Espesor [cm]']/100), ("AA", geo['Ancho panel [cm]']/100), ("DELTA", geo['Distancia entre lamelas [cm]']/100), ("NUML", geo['Número de lamelas'])):
                    line = line.replace(var[0], str(round(var[1], 6)))
            else:
                if tipo == "No estructurada":
                    line = line.replace("Recombine", "//Recombine")
            contenido += line
    with open(nom_geo, "w+", encoding="utf-8", errors = "ignore") as file:
        file.write(contenido)
    
    #Generación de msh
    primera = True
    if DEM:
        dirs = ("OpenFOAM", "CFD_DEM")
    else:
        dirs = ("OpenFOAM",)
    for dir in dirs:
        comandos = ("gmsh -3 " + nom_geo + " -o ./" + dir + "/geometria.msh -format msh2", "meshio-convert ./" + dir + "/geometria.msh out.vtk", "gmsh ./" + dir + "/geometria.msh")
        for comando in comandos:
            if comando != comandos[-1] or primera: 
                proc = subprocess.run(comando.split(" "))
            if comando == comandos[-1] and primera:
                primera = False
    comando = "rm -rf " + nom_geo
    proc = subprocess.run(comando.split(" "))
    
    #Observar vtk
    guardar()

def guardar(file="out.vtk"):
    saved_file = file
    dolfin = pv.read(saved_file)
    qual = dolfin.compute_cell_quality()
    qual.plot(show_edges=True)

    #Guardar como imagen
    """
    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(qual)
    plotter.show(screenshot='malla.png')
    """
    

class Geometry():        
    def malla(self, geo, lamela, rango, e, name):
        #Conversión a cm
        geo['DI [m]'] = geo['DI [m]']*100
        e = e/(10**4)
        
        #---Desarrollo de la geometría---
        with pygmsh.occ.Geometry() as geom:
            #Tamaño de malla
            geom.characteristic_length_min = rango[0]/(10**3)
            geom.characteristic_length_max = rango[1]/(10**3)
            
            #Desarrollo de la geometría
            long = geo['DI [m]']/2
            entrada = geom.add_rectangle([0, 0, 0], geo['DI [m]'], long)
            lodos = geom.add_rectangle([0,long,0], 1.5*geo['DI [m]'], geo['Ancho panel [cm]'])
            salida = geom.add_polygon([
                [0, long + geo['Ancho panel [cm]']],
                [-geo['Altura panel [cm]']*sin(radians(geo['Inclinación [°]'])), geo['Altura panel [cm]']*cos(radians(geo['Inclinación [°]'])) + long + geo['Ancho panel [cm]']],
                [-geo['Altura panel [cm]']*sin(radians(geo['Inclinación [°]'])), geo['Altura panel [cm]']*cos(radians(geo['Inclinación [°]'])) + long + geo['Ancho panel [cm]'] - geo["Ancho lamela [cm]"]],
                [0, long + geo['Ancho panel [cm]'] - geo["Ancho lamela [cm]"]]
            ], mesh_size=rango[0]/(10**3))
            #disk1 = geom.add_disk([-1.2, 0.0, 0.0], 0.5)
            #disk2 = geom.add_disk([+1.2, 0.0, 0.0], 0.5)

            #disk3 = geom.add_disk([0.0, -0.9, 0.0], 0.5)
            #disk4 = geom.add_disk([0.0, +0.9, 0.0], 0.5)

            flat = geom.boolean_union([entrada, lodos])

            top, volume, lat = geom.extrude(flat, [0, 0, e], recombine=True)
            
            #Nombres de las Fronteras
            geom.add_physical(flat, label="bottom") 
            geom.add_physical(top, label="top") 
            #geom.add_physical(volume, label="volume") 
            geom.add_physical(lat[0], label="lat")
            
            #geom.add_raw_code('Mesh.RecombinationAlgorithm=2;\n')
            
            mesh = geom.generate_mesh(dim=2)
            
            mesh.write(name)
            nombre = name.replace(".vtk", ".stl")
            mesh.write(nombre, file_format="stl")
            #meshio.ansys.write(nombre, mesh, binary=False)
    
    def guardar(self, file="out.msh"):
        saved_file = file
        dolfin = pv.read(saved_file)
        qual = dolfin.compute_cell_quality()
        qual.plot(show_edges=True)
        
        #Guardar como imagen
        """
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(qual)
        plotter.show(screenshot='malla.png')
        """
    
    def convertir(self, file="out"):
        saved_file = os.getcwd() + '/' + file
        dolfin = pv.read(saved_file)
        qual = dolfin.compute_cell_quality()
        #self.convertir()
        qual.plot(show_edges=True)
        root =  os.getcwd() + '/'
        read = meshio.read(
            root + file + '.vtk'
        )
        meshio.ansys.write(
            root + file + '.msh',
            binary = False            
        )