import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

# Definimos las funciones

def alfa_m(v):
    return 0.1 * (v + 40) / (1 - np.exp(-(v + 40) / 10))

def beta_m(v):
    return 4 * np.exp(-(v + 65) / 18)

def alfa_n(v):
    return 0.01 * (v + 55) / (1 - np.exp(-(v + 55) / 10))

def beta_n(v):
    return 0.125 * np.exp(-(v + 65) / 80)

def alfa_h(v):
    return 0.07 * np.exp(-(v + 65) / 20)

def beta_h(v):
    return 1 / (1 + np.exp(-(v + 35) / 10))

def HH(ek, el, ena, gna, gk, gl, i):
    def HH(v, t):
        m = alfa_m(v) / (alfa_m(v) + beta_m(v))
        n = alfa_n(v) / (alfa_n(v) + beta_n(v))
        h = alfa_h(v) / (alfa_h(v) + beta_h(v))
        dv = (i(t) - gna * m ** 3 * h * (v - ena) - gk * n ** 4 * (v - ek) - gl * (v - el)) / 1
        return dv
    return HH


def solucionRungeKutta2(t, gk, gna, gl, ek, ena, el):
    v = np.zeros(len(t))
    v[0] = 0
    for i in range(1, len(t)):
        dv1 = HH(v[i - 1], gk, gna, gl, ek, ena, el, t[i - 1])
        dv2 = HH(v[i - 1] + dv1 * (t[i] - t[i - 1]) / 2, gk, gna, gl, ek, ena, el, t[i - 1] + (t[i] - t[i - 1]) / 2)
        v[i] = v[i - 1] + (dv1 + dv2) * (t[i] - t[i - 1]) / 2
    return v

def solucionRungeKutta4(v0, t, gk, gna, gl, vk, vna, vl, i):
    v = np.zeros(len(t))
    v[0] = v0
    for i in range(1, len(t)):
        dv1 = HH(v[i - 1], t[i - 1], gk, gna, gl, vk, vna, vl, i)
        dv2 = HH(v[i - 1] + dv1 * (t[i] - t[i - 1]) / 2, t[i - 1] + (t[i] - t[i - 1]) / 2, gk, gna, gl, vk, vna, vl, i)
        dv3 = HH(v[i - 1] + dv2 * (t[i] - t[i - 1]) / 2, t[i - 1] + (t[i] - t[i - 1]) / 2, gk, gna, gl, vk, vna, vl, i)
        dv4 = HH(v[i - 1] + dv3 * (t[i] - t[i - 1]), t[i - 1] + (t[i] - t[i - 1]), gk, gna, gl, vk, vna, vl, i)
        v[i] = v[i - 1] + (dv1 + 2 * dv2 + 2 * dv3 + dv4) * (t[i] - t[i - 1]) / 6
    return v

def solucionEulerForward(v0, t, gk, gna, gl, vk, vna, vl, i):
    v = np.zeros(len(t))
    v[0] = v0
    for i in range(1, len(t)):
        dv = HH(v[i - 1], t[i - 1], gk, gna, gl, vk, vna, vl, i)
        v[i] = v[i - 1] + dv * (t[i] - t[i - 1])
    return v

def solucionEulerBackward(v0, t, gk, gna, gl, vk, vna, vl, i):
    v = np.zeros(len(t))
    v[0] = v0
    for i in range(1, len(t)):
        dv = HH(v[i - 1], t[i - 1], gk, gna, gl, vk, vna, vl, i)
        v[i] = v[i - 1] + dv * (t[i] - t[i - 1])
    return v

def solucionScipy(v0, t, gk, gna, gl, vk, vna, vl, i):
    sol = solve_ivp(HH, [t[0], t[-1]], [v0], t_eval=t, args=(gk, gna, gl, vk, vna, vl, i))
    return sol.y[0]




