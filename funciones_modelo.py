import pylab as plt
import numpy as np
from scipy.integrate import odeint

class HodgkinHuxley():
    
    def __init__(self, cm, gna, gk, gl, ena, ek, el, tiempoInicio, tiempoFinal, h, metodo):
        """
        Parametros
        |  :param cm: membrana de capacitancia, en uF/cm^2
        |  :param gna: conductancia maxima de sodio (Na), en mS/cm^2
        |  :param gk: conductancia maxima de potasio (K), en mS/cm^2
        |  :param gl: conductancia maxima de la fuga, en mS/cm^2
        |  :param ena: potencial de reversa de sodio (Na = nombre del elemento), en mV
        |  :param ek: potencial de reversa de potasio (K = nombre del elemento), en mV
        |  :param el: potencial de reversa de la fuga, en mV
        |  :param tiempoInicio: tiempo de inicio
        |  :param tiempoFinal: tiempo final
        |  :param h: paso de tiempo
        """

        self.cm = cm
        
        self.gna = gna
        
        self.gk = gk
        
        self.gl = gl
        
        self.ena = ena
        
        self.ek = ek
        
        self.el = el
        
        self.t = np.arange(tiempoInicio, tiempoFinal + h, h)

        self.metodo = metodo
        

    def alfa_m(self, V):
        """
        Parametros
        |  :param V: potencial de membrana
        |  :return: alfa_m
        """

        return 0.1*(V+40.0)/(1.0 - np.exp(-(V+40.0) / 10.0))

    def beta_m(self, V):
        """
        Parametros
        |  :param V: potencial de membrana
        |  :return: beta_m
        """

        return 4.0*np.exp(-(V+65.0) / 18.0)

    def alfa_h(self, V):
        """
        Parametros
        |  :param V: potencial de membrana
        |  :return: alfa_h
        """

        return 0.07*np.exp(-(V+65.0) / 20.0)

    def beta_h(self, V):
        """
        Parametros
        |  :param V: potencial de membrana
        |  :return: beta_h
        """
        
        return 1.0/(1.0 + np.exp(-(V+35.0) / 10.0))

    def alfa_n(self, V):
        """
        Parametros
        |  :param V: potencial de membrana
        |  :return: alfa_n
        """

        return 0.01*(V+55.0)/(1.0 - np.exp(-(V+55.0) / 10.0))

    def beta_n(self, V):
        """
        Parametros
        |  :param V: potencial de membrana
        |  :return: beta_n
        """

        return 0.125*np.exp(-(V+65) / 80.0)

    def I_Na(self, V, m, h):
        """
        Parametros
        |  :param V: potencial de membrana
        |  :param m: variable de estado
        |  :param h: variable de estado
        |  :return: corriente de sodio
        """

        return self.gna * m**3 * h * (V - self.ena)

    def I_K(self, V, n):
        """
        Parametros
        |  :param V: potencial de membrana
        |  :param n: variable de estado
        |  :return: corriente de potasio
        """

        return self.gk  * n**4 * (V - self.ek)
    #  Leak
    def I_L(self, V):
        """
        Parametros
        |  :param V: potencial de membrana
        |  :return: corriente de fuga
        """

        return self.gl * (V - self.el)

    def I_inj(self, t):
        """
        Parametros
        |  :param t: tiempo
        |  :return: corriente de inyeccion
        """

        if (t>=10) and (t<=50):
            return 20
        elif (t>=100) and (t<=150):
            return 120
        elif (t>=300) and (t<=350):
            return -10
        else:
            return 0

    @staticmethod
    def dALLdt(X, t, self):
        """
        Parametros
        |  :param X: vector de variables de estado
        |  :param t: tiempo
        |  :param self:
        |  :return: derivadas de las variables de estado
        """
        V, m, h, n = X

        dVdt = (self.I_inj(t) - self.I_Na(V, m, h) - self.I_K(V, n) - self.I_L(V)) / self.cm
        dmdt = self.alfa_m(V)*(1.0-m) - self.beta_m(V)*m
        dhdt = self.alfa_h(V)*(1.0-h) - self.beta_h(V)*h
        dndt = self.alfa_n(V)*(1.0-n) - self.beta_n(V)*n
        return dVdt, dmdt, dhdt, dndt

    def rungeKutta2(self, X, t):
        """
        Parametros
        |  :param X: vector de variables de estado
        |  :param t: tiempo
        |  :param self:
        |  :return: vector de variables de estado
        """

        k1 = self.dALLdt(X, t, self)
        k2 = self.dALLdt(X + 0.5 * k1, t + 0.5 * self.h, self)
        return X + k2 * self.h

    def rungeKutta4(self, X, t):
        """
        Parametros
        |  :param X: vector de variables de estado
        |  :param t: tiempo
        |  :param self:
        |  :return: vector de variables de estado
        """

        k1 = self.dALLdt(X, t, self)
        k2 = self.dALLdt(X + 0.5 * k1, t + 0.5 * self.h, self)
        k3 = self.dALLdt(X + 0.5 * k2, t + 0.5 * self.h, self)
        k4 = self.dALLdt(X + k3, t + self.h, self)
        return X + (k1 + 2.0 * k2 + 2.0 * k3 + k4) * self.h / 6.0

    def Main(self):
        """
        Main del programa principal
        """
        if self.metodo == "odeint":
            X = odeint(self.dALLdt, [-65, 0.05, 0.5, 0.4], self.t, args=(self,))
            V = X[:,0]
            m = X[:,1]
            h = X[:,2]
            n = X[:,3]
            ina = self.I_Na(V, m, h)
            ik = self.I_K(V, n)
            il = self.I_L(V)
        
        elif self.metodo == "rungeKutta2":
            X = np.zeros((len(self.t), 4))
            X[0] = [-65, 0.05, 0.5, 0.4]
            for i in range(1, len(self.t)):
                X[i] = self.rungeKutta2(X[i-1], self.t[i-1])
            V = X[:,0]
            m = X[:,1]
            h = X[:,2]
            n = X[:,3]
            ina = self.I_Na(V, m, h)
            ik = self.I_K(V, n)
            il = self.I_L(V)
        
        elif self.metodo == "rungeKutta4":
            X = np.zeros((len(self.t), 4))
            X[0] = [-65, 0.05, 0.5, 0.4]
            for i in range(1, len(self.t)):
                X[i] = self.rungeKutta4(X[i-1], self.t[i-1])
            V = X[:,0]
            m = X[:,1]
            h = X[:,2]
            n = X[:,3]
            ina = self.I_Na(V, m, h)
            ik = self.I_K(V, n)
            il = self.I_L(V)
        
        else:
            print("Metodo no valido")
            return

        plt.figure()

        ax1 = plt.subplot(4,1,1)
        plt.title('Hodgkin-Huxley Neuron')
        plt.plot(self.t, V, 'k')
        plt.ylabel('V (mV)')

        plt.subplot(4,1,2, sharex = ax1)
        plt.plot(self.t, ina, 'c', label='$I_{Na}$')
        plt.plot(self.t, ik, 'y', label='$I_{K}$')
        plt.plot(self.t, il, 'm', label='$I_{L}$')
        plt.ylabel('Current')
        plt.legend()

        plt.subplot(4,1,3, sharex = ax1)
        plt.plot(self.t, m, 'r', label='m')
        plt.plot(self.t, h, 'g', label='h')
        plt.plot(self.t, n, 'b', label='n')
        plt.ylabel('Gating Value')
        plt.legend()

        plt.subplot(4,1,4, sharex = ax1)
        i_inj_values = [self.I_inj(t) for t in self.t]
        plt.plot(self.t, i_inj_values, 'k')
        plt.xlabel('t (ms)')
        plt.ylabel('$I_{inj}$ ($\\mu{A}/cm^2$)')
        plt.ylim(-1, 40)

        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    runner = HodgkinHuxley(1, 120, 36, 0.3, 50, -77, -54.387, 0, 500, 0.01, "rungeKutta2")
    runner.Main()
