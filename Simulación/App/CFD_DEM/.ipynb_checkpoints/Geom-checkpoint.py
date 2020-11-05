import pyvista as pv
import pygmsh
import ipywidgets as widgets
from math import pi, radians, cos, sin, tan
import meshio

def Rango(minimo=250, maximo=10000):
    Req = widgets.IntRangeSlider(
        value=[minimo, 5*minimo],
        min=minimo,
        max=maximo,
        step=1,
        description='Rango [um]:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True
    )
    return Req

def Malla():
    Req = Rango()
    tab = widgets.Tab()
    tab.children = [Req]
    tab.set_title(0, 'Tamaño de malla')
    return tab

def Dibujar(geo, lamela, rango, e, name ="out.vtk"):
    g = Geometry()
    g.malla(geo, lamela, rango, e, name)
    g.guardar(name)
    

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

            top, volume, lat = geom.extrude(flat, [0, 0, e])
            
            #Nombres de las Fronteras
            geom.add_physical(flat, label="bottom") 
            geom.add_physical(top, label="top") 
            #geom.add_physical(volume, label="volume") 
            #geom.add_physical(lat, label="lat")
            print(volume.__attr__)
            
            mesh = geom.generate_mesh()
            
            mesh.write(name)
            nombre = name.replace(".vtk", ".msh")
            mesh.write(nombre, file_format="gmsh22")
    
    def guardar(self, file="out.msh"):
        saved_file = file
        dolfin = pv.read(saved_file)
        qual = dolfin.compute_cell_quality()
        qual.plot(show_edges=True)
    
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
        meshio.write(
            root + file + '.msh',
            read            
        )