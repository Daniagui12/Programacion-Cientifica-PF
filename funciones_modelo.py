import pylab as plt
import numpy as np
from scipy.integrate import odeint
import scipy.optimize as opt

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

        self.h = h
        
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


    def dVdtFunction(self, V, n, m, h, t):
        """
        Parametros
        |  :param X: vector de variables de estado
        |  :param t: tiempo
        |  :param self:
        |  :return: derivada del potencial de membrana
        """
        return (self.I_inj(t) - self.I_Na(V, m, h) - self.I_K(V, n) - self.I_L(V)) / self.cm
    
    # Derivada respecto a V
    def f_v(self, V, n, m, h, t):
        """
        Parametros
        |  :param X: vector de variables de estado
        |  :param t: tiempo
        |  :param self:
        |  :return: derivada de la funcion respecto a V
        """
        return (-self.I_Na(V, m, h) - self.I_K(V, n) - self.I_L(V)) / self.cm
    
    # Derivada respecto a n
    def f_n(self, V, n):
        """
        Parametros
        |  :param X: vector de variables de estado
        |  :param t: tiempo
        |  :param self:
        |  :return: derivada de la funcion respecto a n
        """
        return self.gk * (4 * n**3) * (V - self.ek)
    
    # Derivada respecto a m
    def f_m(self, V, m, h):
        """
        Parametros
        |  :param X: vector de variables de estado
        |  :param t: tiempo
        |  :param self:
        |  :return: derivada de la funcion respecto a m
        """
        return self.gna * (3 * m**2) * h * (V - self.ena)
    
    # Derivada respecto a h
    def f_h(self, V, m):
        """
        Parametros
        |  :param X: vector de variables de estado
        |  :param t: tiempo
        |  :param self:
        |  :return: derivada de la funcion respecto a h
        """
        return self.gna * m**3 * (V - self.ena)

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

    def FEulerBackRoot(self, arraySolutions, v, n, m, h, t):
        """
        Parametros
        |  :param arraySolutions: vector de variables de estado
        |  :param v: potencial de membrana
        |  :param n: variable de estado n
        |  :param m: variable de estado m
        |  :param h: variable de estado h
        |  :param t: tiempo
        |  :return: vector de variables de estado
        """
        return [v + self.h * self.dVdtFunction(arraySolutions[0], arraySolutions[1], arraySolutions[2], arraySolutions[3], t) - arraySolutions[0],
                n + self.h * (self.alfa_n(arraySolutions[0])*(1.0-arraySolutions[1]) - self.beta_n(arraySolutions[0])*arraySolutions[1]) - arraySolutions[1],
                m + self.h * (self.alfa_m(arraySolutions[0])*(1.0-arraySolutions[2]) - self.beta_m(arraySolutions[0])*arraySolutions[2]) - arraySolutions[2],
                h + self.h * (self.alfa_h(arraySolutions[0])*(1.0-arraySolutions[3]) - self.beta_h(arraySolutions[0])*arraySolutions[3]) - arraySolutions[3]]

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
            return V, ina, ik, il
        
        elif self.metodo == "rungeKutta2":
            v_RK2 = np.zeros(len(self.t))
            n_RK2 = np.zeros(len(self.t))
            m_RK2 = np.zeros(len(self.t))
            h_RK2 = np.zeros(len(self.t))
            v_RK2[0] = -65
            n_RK2[0] = 0.05
            m_RK2[0] = 0.5
            h_RK2[0] = 0.4
            for i in range(1, len(self.t)):
                vk11 = self.dVdtFunction(v_RK2[i - 1], n_RK2[i - 1], m_RK2[i - 1], h_RK2[i - 1], self.t[i - 1])
                nk11 = self.alfa_n(v_RK2[i - 1]) * (1 - n_RK2[i - 1]) - self.beta_n(v_RK2[i - 1]) * n_RK2[i - 1]
                mk11 = self.alfa_m(v_RK2[i - 1]) * (1 - m_RK2[i - 1]) - self.beta_m(v_RK2[i - 1]) * m_RK2[i - 1]
                hk11 = self.alfa_h(v_RK2[i - 1]) * (1 - h_RK2[i - 1]) - self.beta_h(v_RK2[i - 1]) * h_RK2[i - 1]
                vk12 = self.dVdtFunction(v_RK2[i - 1] + 0.5 * self.h * vk11, n_RK2[i - 1] + 0.5 * self.h * nk11, m_RK2[i - 1] + 0.5 * self.h * mk11, h_RK2[i - 1] + 0.5 * self.h * hk11, self.t[i - 1] + 0.5 * self.h)
                nk12 = self.alfa_n(v_RK2[i - 1] + 0.5 * self.h * vk11) * (1 - (n_RK2[i - 1] + 0.5 * self.h * nk11)) - self.beta_n(v_RK2[i - 1] + 0.5 * self.h * vk11) * (n_RK2[i - 1] + 0.5 * self.h * nk11)
                mk12 = self.alfa_m(v_RK2[i - 1] + 0.5 * self.h * vk11) * (1 - (m_RK2[i - 1] + 0.5 * self.h * mk11)) - self.beta_m(v_RK2[i - 1] + 0.5 * self.h * vk11) * (m_RK2[i - 1] + 0.5 * self.h * mk11)
                hk12 = self.alfa_h(v_RK2[i - 1] + 0.5 * self.h * vk11) * (1 - (h_RK2[i - 1] + 0.5 * self.h * hk11)) - self.beta_h(v_RK2[i - 1] + 0.5 * self.h * vk11) * (h_RK2[i - 1] + 0.5 * self.h * hk11)
                v_RK2[i] = v_RK2[i - 1] + self.h * vk12
                n_RK2[i] = n_RK2[i - 1] + self.h * nk12
                m_RK2[i] = m_RK2[i - 1] + self.h * mk12
                h_RK2[i] = h_RK2[i - 1] + self.h * hk12
            V = v_RK2
            m = m_RK2
            h = h_RK2
            n = n_RK2

            ina = self.I_Na(V, m, h)
            ik = self.I_K(V, n)
            il = self.I_L(V)
            return V, ina, ik, il
        
        elif self.metodo == "rungeKutta4":
            v_RK4 = np.zeros(len(self.t))
            n_RK4 = np.zeros(len(self.t))
            m_RK4 = np.zeros(len(self.t))
            h_RK4 = np.zeros(len(self.t))
            v_RK4[0] = -65
            n_RK4[0] = 0.05
            m_RK4[0] = 0.5
            h_RK4[0] = 0.4
            for i in range(1, len(self.t)):
                vk11 = self.dVdtFunction(v_RK4[i - 1], n_RK4[i - 1], m_RK4[i - 1], h_RK4[i - 1], self.t[i - 1])
                nk11 = self.alfa_n(v_RK4[i - 1]) * (1 - n_RK4[i - 1]) - self.beta_n(v_RK4[i - 1]) * n_RK4[i - 1]
                mk11 = self.alfa_m(v_RK4[i - 1]) * (1 - m_RK4[i - 1]) - self.beta_m(v_RK4[i - 1]) * m_RK4[i - 1]
                hk11 = self.alfa_h(v_RK4[i - 1]) * (1 - h_RK4[i - 1]) - self.beta_h(v_RK4[i - 1]) * h_RK4[i - 1]
                vk12 = self.dVdtFunction(v_RK4[i - 1] + 0.5 * self.h * vk11, n_RK4[i - 1] + 0.5 * self.h * nk11, m_RK4[i - 1] + 0.5 * self.h * mk11, h_RK4[i - 1] + 0.5 * self.h * hk11, self.t[i - 1] + 0.5 * self.h)
                nk12 = self.alfa_n(v_RK4[i - 1] + 0.5 * self.h * vk11) * (1 - (n_RK4[i - 1] + 0.5 * self.h * nk11)) - self.beta_n(v_RK4[i - 1] + 0.5 * self.h * vk11) * (n_RK4[i - 1] + 0.5 * self.h * nk11)
                mk12 = self.alfa_m(v_RK4[i - 1] + 0.5 * self.h * vk11) * (1 - (m_RK4[i - 1] + 0.5 * self.h * mk11)) - self.beta_m(v_RK4[i - 1] + 0.5 * self.h * vk11) * (m_RK4[i - 1] + 0.5 * self.h * mk11)
                hk12 = self.alfa_h(v_RK4[i - 1] + 0.5 * self.h * vk11) * (1 - (h_RK4[i - 1] + 0.5 * self.h * hk11)) - self.beta_h(v_RK4[i - 1] + 0.5 * self.h * vk11) * (h_RK4[i - 1] + 0.5 * self.h * hk11)
                vk13 = self.dVdtFunction(v_RK4[i - 1] + 0.5 * self.h * vk12, n_RK4[i - 1] + 0.5 * self.h * nk12, m_RK4[i - 1] + 0.5 * self.h * mk12, h_RK4[i - 1] + 0.5 * self.h * hk12, self.t[i - 1] + 0.5 * self.h)
                nk13 = self.alfa_n(v_RK4[i - 1] + 0.5 * self.h * vk12) * (1 - (n_RK4[i - 1] + 0.5 * self.h * nk12)) - self.beta_n(v_RK4[i - 1] + 0.5 * self.h * vk12) * (n_RK4[i - 1] + 0.5 * self.h * nk12)
                mk13 = self.alfa_m(v_RK4[i - 1] + 0.5 * self.h * vk12) * (1 - (m_RK4[i - 1] + 0.5 * self.h * mk12)) - self.beta_m(v_RK4[i - 1] + 0.5 * self.h * vk12) * (m_RK4[i - 1] + 0.5 * self.h * mk12)
                hk13 = self.alfa_h(v_RK4[i - 1] + 0.5 * self.h * vk12) * (1 - (h_RK4[i - 1] + 0.5 * self.h * hk12)) - self.beta_h(v_RK4[i - 1] + 0.5 * self.h * vk12) * (h_RK4[i - 1] + 0.5 * self.h * hk12)
                vk14 = self.dVdtFunction(v_RK4[i - 1] + self.h * vk13, n_RK4[i - 1] + self.h * nk13, m_RK4[i - 1] + self.h * mk13, h_RK4[i - 1] + self.h * hk13, self.t[i - 1] + self.h)
                nk14 = self.alfa_n(v_RK4[i - 1] + self.h * vk13) * (1 - (n_RK4[i - 1] + self.h * nk13)) - self.beta_n(v_RK4[i - 1] + self.h * vk13) * (n_RK4[i - 1] + self.h * nk13)
                mk14 = self.alfa_m(v_RK4[i - 1] + self.h * vk13) * (1 - (m_RK4[i - 1] + self.h * mk13)) - self.beta_m(v_RK4[i - 1] + self.h * vk13) * (m_RK4[i - 1] + self.h * mk13)
                hk14 = self.alfa_h(v_RK4[i - 1] + self.h * vk13) * (1 - (h_RK4[i - 1] + self.h * hk13)) - self.beta_h(v_RK4[i - 1] + self.h * vk13) * (h_RK4[i - 1] + self.h * hk13)
                v_RK4[i] = v_RK4[i - 1] + (self.h / 6) * (vk11 + 2 * vk12 + 2 * vk13 + vk14)
                n_RK4[i] = n_RK4[i - 1] + (self.h / 6) * (nk11 + 2 * nk12 + 2 * nk13 + nk14)
                m_RK4[i] = m_RK4[i - 1] + (self.h / 6) * (mk11 + 2 * mk12 + 2 * mk13 + mk14)
                h_RK4[i] = h_RK4[i - 1] + (self.h / 6) * (hk11 + 2 * hk12 + 2 * hk13 + hk14)
            
            V = v_RK4
            m = m_RK4
            h = h_RK4
            n = n_RK4

            ina = self.I_Na(V, m, h)
            ik = self.I_K(V, n)
            il = self.I_L(V)
            return V, ina, ik, il


        elif self.metodo == "eulerFor":
            v_e = np.zeros(len(self.t))
            n_e = np.zeros(len(self.t))
            m_e = np.zeros(len(self.t))
            h_e = np.zeros(len(self.t))
            v_e[0] = -65
            n_e[0] = 0.05
            m_e[0] = 0.5
            h_e[0] = 0.4
            for i in range(1, len(self.t)):
                v_e[i] = v_e[i - 1] + self.h * self.dVdtFunction(v_e[i - 1], n_e[i - 1], m_e[i - 1], h_e[i - 1], self.t[i])
                n_e[i] = n_e[i - 1] + self.h * (self.alfa_n(v_e[i - 1]) * (1.0-n_e[i - 1]) - self.beta_n(v_e[i - 1]) * n_e[i - 1])
                m_e[i] = m_e[i - 1] + self.h * (self.alfa_m(v_e[i - 1]) * (1.0-m_e[i - 1]) - self.beta_m(v_e[i - 1]) * m_e[i - 1])
                h_e[i] = h_e[i - 1] + self.h * (self.alfa_h(v_e[i - 1]) * (1.0-h_e[i - 1]) - self.beta_h(v_e[i - 1]) * h_e[i - 1])
            V = v_e
            m = m_e
            h = h_e
            n = n_e
            ina = self.I_Na(V, m, h)
            ik = self.I_K(V, n)
            il = self.I_L(V)
            return V, ina, ik, il
        
        elif self.metodo == "eulerBack":
            v_eBack = np.zeros(len(self.t))
            n_eBack = np.zeros(len(self.t))
            m_eBack = np.zeros(len(self.t))
            h_eBack = np.zeros(len(self.t))
            v_eBack[0] = -65
            n_eBack[0] = 0.05
            m_eBack[0] = 0.5
            h_eBack[0] = 0.4
            for i in range(1, len(self.t)):
                v_eBack[i] = self.f_v(v_eBack[i - 1], n_eBack[i - 1], m_eBack[i - 1], h_eBack[i - 1], self.t[i])
                n_eBack[i] = self.f_n(n_eBack[i - 1], v_eBack[i - 1])
                m_eBack[i] = self.f_m(m_eBack[i - 1], v_eBack[i - 1], h_eBack[i - 1])
                h_eBack[i] = self.f_h(h_eBack[i - 1], v_eBack[i - 1])

            V = v_eBack
            m = m_eBack
            h = h_eBack
            n = n_eBack
            ina = self.I_Na(V, m, h)
            ik = self.I_K(V, n)
            il = self.I_L(V)
            return V, ina, ik, il

        elif self.metodo == "eulerMod":
            v_eMod = np.zeros(len(self.t))
            n_eMod = np.zeros(len(self.t))
            m_eMod = np.zeros(len(self.t))
            h_eMod = np.zeros(len(self.t))
            v_eMod[0] = -65
            n_eMod[0] = 0.05
            m_eMod[0] = 0.5
            h_eMod[0] = 0.4
            for i in range(1, len(self.t)):
                solMod = opt.fsolve(self.FEulerBackRoot,
                     np.array([v_eMod[i - 1],
                               n_eMod[i - 1],
                               m_eMod[i - 1],
                               h_eMod[i - 1]]),
                (
                    v_eMod[i - 1],
                    n_eMod[i - 1],
                    m_eMod[i - 1],
                    h_eMod[i - 1], self.t[i]), xtol=10 ** -15)
            
                v_eMod[i] = solMod[0]
                n_eMod[i] = solMod[1]
                m_eMod[i] = solMod[2]
                h_eMod[i] = solMod[3]
            V = v_eMod
            m = m_eMod
            h = h_eMod
            n = n_eMod

            ina = self.I_Na(V, m, h)
            ik = self.I_K(V, n)
            il = self.I_L(V)
            return V, ina, ik, il

        else:
            print("Metodo no valido")
            return

        # plt.figure()

        # ax1 = plt.subplot(4,1,1)
        # plt.title('Hodgkin-Huxley Neuron')
        # plt.plot(self.t, V, 'k')
        # plt.ylabel('V (mV)')

        # plt.subplot(4,1,2, sharex = ax1)
        # plt.plot(self.t, ina, 'c', label='$I_{Na}$')
        # plt.plot(self.t, ik, 'y', label='$I_{K}$')
        # plt.plot(self.t, il, 'm', label='$I_{L}$')
        # plt.ylabel('Current')
        # plt.legend()

        # plt.subplot(4,1,3, sharex = ax1)
        # plt.plot(self.t, m, 'r', label='m')
        # plt.plot(self.t, h, 'g', label='h')
        # plt.plot(self.t, n, 'b', label='n')
        # plt.ylabel('Gating Value')
        # plt.legend()

        # plt.subplot(4,1,4, sharex = ax1)
        # i_inj_values = [self.I_inj(t) for t in self.t]
        # plt.plot(self.t, i_inj_values, 'k')
        # plt.xlabel('t (ms)')
        # plt.ylabel('$I_{inj}$ ($\\mu{A}/cm^2$)')
        # plt.ylim(-1, 40)

        # plt.tight_layout()
        # plt.show()

if __name__ == '__main__':
    runner = HodgkinHuxley(1, 120, 36, 0.3, 50, -77, -54.387, 0, 500, 0.01, "eulerMod")
    runner.Main()
