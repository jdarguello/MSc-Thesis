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
        NbW = np.linspace(NbWlimit/10, NbWlimit, puntos)
        Cs = np.linspace(CSmin, CSmax, puntos)
        var = {
            'N': np.linspace(1, Nlimit, Nlimit),
            'W': np.arange(Wlimit/Nlimit, Wlimit + Wlimit/Nlimit, Wlimit/Nlimit),
            'Q': Q,
            'L': L,
            'b': b,
            'theta': theta,
            'mu': mu
        }
        #meshgrids
        NbW, Cs = np.meshgrid(NbW, Cs)
        Q = Cs*NbW*np.cos(theta*pi/180)*(Lb+tan(theta*pi/180))
        for key in var:
            if key != 'N' and key != 'W':
                var[key] = self.vectorizar(var[key], Nlimit)
            var[key] = np.meshgrid(var[key])
        #Calcular carga superficial y Reynolds
        CS = []
        Re = []
        for i in range(len(N)):
            filaCS = []
            filaRe = []
            for j in range(len(N[i])):
                filaCS.append(self.cargaS(Q, N[i][j], L, b, theta, W[i][j]))
                filaRe.append(self.Reynolds(Q, N[i][j], W[i][j], mu))
            CS.append(np.array(filaCS))
            Re.append(np.array(filaRe))
        CS = np.array(CS)
        Re = np.array(Re)
        #CS = self.cargaS(var['Q'], var['N'], var['L'], var['b'], var['theta'], var['W'])
        #Re = self.Re(var['Q'], var['N'], var['W'], var['mu'])
        #Desarrollar gráfica
        self.graph(N, W, CS, Re)
    
    def Reynolds(self, Q, N, W, mu):
        return Q/(N*W*mu)
    
    def cargaS(self, Q, N, L, b, theta, W):
        return Q/(N*((L/b)+np.tan(theta*pi/180))*b*W*np.cos(theta*pi/180))
    
    def graph(self, N, W, CS, Re, cuarta = False):
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
        self.ax.set_xlabel("Número de lamelas")
        self.ax.set_ylabel("W [m]")
        self.ax.set_zlabel("Carga superficial [m/s]")
        plt.show()
    
    def vectorizar(self, var, limit):
        newV = []
        for i in range(limit):
            newV.append(var)
        return np.array(newV)
        
        