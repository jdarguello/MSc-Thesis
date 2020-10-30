import pyvista as pv
import pygmsh
import os
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

            geom.extrude(flat, [0, 0, e])
            
            mesh = geom.generate_mesh()
            
            #mesh.write( os.getcwd() + "/" + name)
            format = "vtk"
            nombre = name.replace(".vtk", "")
            mesh.write(os.getcwd() + "/" + nombre + '.' + format, file_format=format)
            
            """
            for cell in mesh.cells:
                if cell.type == "triangle":
                    triangle_cells = cell.data
                elif  cell.type == "tetra":
                    tetra_cells = cell.data
            print(mesh.cell_data_dict)
            triangle_mesh =meshio.Mesh(points=mesh.points,vt
                           cells=[("triangle", triangle_cells)],
                           cell_data={"name_to_read":[triangle_data]})

            meshio.write("mf.xdmf", triangle_mesh)
            #meshio.write(name, meshio.Mesh(points=mesh.points, cells={"triangle": mesh.cells["triangle"]}, cell_data={"triangle": {"name_to_read": mesh.cell_data["triangle"]["gmsh:physical"]}}))
            """
    
    def guardar(self, file="out.msh"):
        saved_file = os.getcwd() + '/' + file
        dolfin = pv.read(saved_file)
        qual = dolfin.compute_cell_quality()
        #self.convertir()
        qual.plot(show_edges=True)
    
    def convertir(self, file="out"):
        root =  os.getcwd() + '/'
        read = meshio.read(
            root + file + '.vtk'
        )
        meshio.write(
            root + file + '.msh',
            read            
        )