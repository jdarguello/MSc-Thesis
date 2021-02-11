from math import tan, sin, cos, pi
import numpy as np

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

"""
    Objetivo: desarrollar el diagrama 3D entre Cs, Q y NbW. Se emplea bar color del número de Reynolds de la lamela para garantizar flujo laminar.
    
    Cs -> Carga superficial - y
    N b W -> Área de entrada Total - N L b W - x
    Q -> Caudal -z
    
    theta constante = 60ª
    L/b constante = 8
"""    

class Geometria():
    """
        Define la geometría del panel en términos del número de lamelas y del ancho del panel.
    """
    def __init__(self, Q, L, b, theta, mu, NbWlimit=0.0375, CSmin = 6, CSmax = 180, puntos = 100):
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')
        #---Datos---
        ms = 1/24*1/3600
        NbW = np.linspace(NbWlimit/10, NbWlimit, puntos)
        Cs = np.linspace(CSmin, CSmax, puntos)
        
        #meshgrids
        NbW, Cs = np.meshgrid(NbW, Cs)
        Lb = L/b
        Q = ((Cs*ms)*NbW*np.cos(theta*pi/180)*(Lb+tan(theta*pi/180)))*1000*60
        self.graph(NbW, Cs, Q, 0)
    
    def Reynolds(self, Q, N, W, mu):
        return Q/(N*W*mu)
    
    def cargaS(self, Q, N, L, b, theta, W):
        return Q/(N*((L/b)+np.tan(theta*pi/180))*b*W*np.cos(theta*pi/180))
    
    def graph(self, X, Y, Z, C, cuarta = False):
        N = X
        W = Y
        CS = Z
        Re = C
        
        
        #Color
        cmap = cm.jet
        if cuarta:
            color_dimension = Re # change to desired fourth dimension
            minn, maxx = color_dimension.min(), color_dimension.max()
            norm = matplotlib.colors.Normalize(vmin=minn, vmax=maxx)
            m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
            m.set_array([])
            fcolors = m.to_rgba(color_dimension)
            # Plot the surface.
            fcolor = plt.cm.jet((norm(color_dimension)))
            surf = self.ax.plot_surface(N, W, CS,
                                   linewidth=0, antialiased=False, 
                                   facecolors=fcolor)
        else:
            surf = self.ax.plot_surface(N, W, CS,
                                   linewidth=0, antialiased=False, 
                                   cmap = cmap)

        # Customize the z axis.
        limits = [CS[0][0], CS[0][0]]
        for val in CS[0]:
            if val < limits[0]:
                limits[0] = val
            if val > limits[1]:
                limits[1] = val
        self.ax.set_zlim(limits[0], limits[1])
        self.ax.zaxis.set_major_locator(LinearLocator(10))
        self.ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        if cuarta:
            plt.colorbar(m)
        self.ax.set_xlabel("NbW [m2]")
        self.ax.set_ylabel("Carga superficial [m/d]")
        self.ax.set_zlabel("Q [L/min]")
        plt.show()
    
    def vectorizar(self, var, limit):
        newV = []
        for i in range(limit):
            newV.append(var)
        return np.array(newV)
        
        