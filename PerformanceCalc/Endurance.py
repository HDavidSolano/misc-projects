# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 00:05:26 2017

@author: David
"""
import pandas as pd
import math as m
import matplotlib.pyplot as plt
import numpy as np
class esc(object):
    amps = None
    masa = None
    def __init__(self,amp):
        self.amps = amp
        self.masa = 0.8421*amp/1000
class motor(object):        #Estos varian tanto que es mejor buscar los parametros por si mismos
    KV = None
    masa = None
    max_A = None
    max_S = None
    eficiencia = None
    def __init__(self,kv,mass,A,S,E): #Masa se puede dejar como cero si no se conoce o se quiere hacer variar
        self.masa = mass
        if mass == 0:
            self.masa = (10**(4.0499))*(kv**(-0.5329))/1000
        self.KV = kv
        self.max_A = A
        self.max_S = S
        self.eficiencia = E
class bateria(object):
    celdas = None
    capacidad = None
    C_rating = 10 #Default para drones pequenos
    masa = None
    voltaje = None
    burst_current = None
    def __init__(self,cel,cap):
        p_1 = 0.026373
        p_2 = 2.0499*10**(-5)
        self.celdas = cel
        self.capacidad = cap
        self.masa = ((p_1*cel+p_2)*self.capacidad)/1000
        self.voltaje = cel*3.4
        self.burst_current = self.C_rating*cap/1000
    def cambiar_C_rating(self,newC): #Si se necesita nuevo C Rating
        self.C_rating = newC
        self.burst_current = newC*self.capacidad/1000
    def cambiar_masa(self,newM): #Si se necesita nueva masa
        self.masa = newM
class helice(object):
    pitch = None
    diametro = None
    composicion = None
    performance = None
    masa = None
    blades = None
    propulsion = []
    tengo_curvas = 0
    def calcular_fuerza(self,RPM,Densidad,Velocidad): 
        #Primero pasamos todo a unidades inglesas porque las porquerias de tablas estan en ingles
        Velocidad = Velocidad*2.23694 # De m/s a mi/h para las tablas
        multiplier = 1
        if self.blades == 3:
            multiplier = 1.275 
        ct_low_low = None
        ct_low_high = None
        ct_high_low = None
        ct_high_high = None
        V_low_low = None
        V_low_high = None
        V_high_low = None
        V_high_high = None
        rpm_low = None
        rpm_high = None
        calculated_low = 0
        calculated_high = 0
        n = RPM/60
        for a_row in self.propulsion:
            if a_row[4]==m.floor(RPM/1000)*1000:
                rpm_low = a_row[4]
                if a_row[0]<=Velocidad:
                    ct_low_low = a_row[1]
                    V_low_low = a_row[0]
                if a_row[0]>=Velocidad and calculated_low == 0:
                    V_low_high = a_row[0]
                    ct_low_high = a_row[1]
                    calculated_low = 1
            if a_row[4]==(m.floor(RPM/1000)+1)*1000:
                rpm_high = a_row[4]
                if a_row[0]<=Velocidad:
                    V_high_low = a_row[0]
                    ct_high_low = a_row[1]
                if a_row[0]>=Velocidad and calculated_high == 0:
                    V_high_high = a_row[0]
                    ct_high_high = a_row[1]
                    calculated_high = 1
        ct_low = ((Velocidad-V_low_low)/(V_low_high-V_low_low))*(ct_low_high-ct_low_low)+ct_low_low
        ct_high = ((Velocidad-V_high_low)/(V_high_high-V_high_low))*(ct_high_high-ct_high_low)+ct_high_low
        ct_final = ((RPM-rpm_low)/(rpm_high-rpm_low))*(ct_high-ct_low)+ct_low
        Velocidad = Velocidad/2.23694 #Volvemos a cambiar la velocidad a lo que era antes
        T = multiplier*ct_final*(Densidad * n**2 * ((self.diametro*0.3048)/12)**4)
        return T
    def __init__(self,p,d,c,bl): #Opciones para composicion son 0 = madera, 1 = plastico, 2 = plastico reforzado con nylon 3 = carbon
        self.pitch = p
        self.diametro = d
        self.composicion = c
        if c == 0:
            p1 = 0.08884
            p2 = 0
        if c == 1:
            p1 = 0.05555
            p2 = 0.2216
        if c == 2:
            p1 = 0.1178
            p2 = -0.3887
        if c == 3:
            p1 = 0.1207
            p2 = -0.5122
        self.masa = (p1*(d**2)+p2*d)/1000
        self.blades = bl
    def insertar_curva(self,direccion): #
        a_row = None
        initial_RPM = 1000
        prop_row = []
        self.performance = pd.read_csv(direccion, sep='\s+', skiprows=15)
        for index, row in self.performance.iterrows():
            if row['V'] == 'PROP':
                self.tengo_curvas = 1
                initial_RPM = initial_RPM + 1000    #Ve a nueva lista
            elif row['V'] != 'V' and row['V'] != '(mph)':
                prop_row.append([float(row['V']),float(row['Ct']),float(row['Cp']),4.44822*float(row['Thrust']),initial_RPM])
        self.propulsion = prop_row
class propulsor(object):           #Reemplaza tanto la helice como el motor
    propulsion = None              #Aca se referencia el CSV que se llama
    corriente = None
    fuerza = None
    corriente = None
    masa = None
    def  __init__(self,direccion,mass):
        self.propulsion = pd.read_csv(direccion) #Va a tener un formato definido:
        self.masa = mass                         #Fuerza,Amps son los headers
    def llamar_corriente(self,fuerza_requerida):
        self.fuerza = fuerza_requerida
        info_L = self.propulsion.loc[(self.propulsion['Fuerza'] <= fuerza_requerida)]
        info_H = self.propulsion.loc[(self.propulsion['Fuerza'] >= fuerza_requerida)]
        A_L = info_L['Amps'][info_L.index.values[-1]]
        A_H = info_H['Amps'][info_H.index.values[0]]
        F_L = info_L['Fuerza'][info_L.index.values[-1]]
        F_H = info_H['Fuerza'][info_H.index.values[0]]
        if F_L == F_H:
            self.corriente = A_L
        else:
            self.corriente = ((fuerza_requerida-F_L)/(F_H-F_L))*(A_H-A_L)+A_L
class Avion(object):
    propulsores = []    #Lista de propulsores en el avion
    motores = []
    escs = []
    baterias = []
    helices = []
    masa_payload = None
    masa_frame = None
    masa_powerplant = None
    area_ala = None
    def  __init__(self,lista_propulsores,lista_motores,lista_escs,lista_baterias,lista_helices,m_payload,m_frame,Warea):        
        self.masa_powerplant = 0
        self.propulsores = lista_propulsores
        self.motores = lista_motores
        self.escs = lista_escs
        self.baterias = lista_baterias
        self.helices = lista_helices
        self.masa_payload = m_payload
        self.masa_frame = m_frame
        for un_motor in lista_motores:
            self.masa_powerplant = self.masa_powerplant + un_motor.masa
        for una_esc in lista_escs:
            self.masa_powerplant = self.masa_powerplant + una_esc.masa               
        for una_bateria in lista_baterias:
            self.masa_powerplant = self.masa_powerplant + una_bateria.masa
        for una_helice in lista_helices:
            self.masa_powerplant = self.masa_powerplant + una_helice.masa
        self.peso_total = 9.81*self.masa_powerplant + 9.81*self.masa_payload + 9.81*self.masa_frame
        self.area_ala = Warea
    def analizar_hand_Launch(self,CL,vel_lanzamiento,alt_lanzamiento,densidad,usar_helices,angulo_lanzamiento,celdas):
        cd = 0.05
        n_steps = 200
        dt = 0.01
        t = 0
        X = []
        Y = []
        TIME_VECTOR = []
        x_0 = [0,alt_lanzamiento]
        Y_Ground = np.zeros(n_steps-1)
        V_Stall = (2*self.peso_total/(densidad*CL*self.area_ala/10))**0.5
        v_0 = [vel_lanzamiento*m.cos(angulo_lanzamiento),vel_lanzamiento*m.sin(angulo_lanzamiento)]
        V = []
        V_REF = []
        #Porque Juanma queria un integrador de persona
        v_1 = [0,0]
        x_1 = [0,0]
        a_1 = [0,0]
        v_2 = [0,0]
        x_2 = [0,0]
        a_2 = [0,0]
        v_3 = [0,0]
        x_3 = [0,0]
        a_3 = [0,0]
        v_4 = [0,0]
        x_4 = [0,0]
        a_4 = [0,0]
        i = 1
        for a_motor in self.motores:
                RPM_lim = a_motor.eficiencia*a_motor.KV*celdas*3.4
        v = v_0
        x = x_0            
        mass = self.peso_total/9.81
        while i < n_steps:
            T = 0
            #Primera iteracion
            v_1[0] = v[0]
            v_1[1] = v[1]
            x_1[0] = x[0]
            x_1[1] = x[1]
            for una_helice in self.helices: #loopea a travez de apc
                v_norm = (v_1[0]**2+v_1[1]**2)**0.5
                T = T+una_helice.calcular_fuerza(RPM_lim,densidad,v_norm)
            L = (0.5*densidad*v_norm**2)*CL*(self.area_ala/10)
            D = (0.5*densidad*v_norm**2)*(cd+(CL**2)/(3.141592*8*0.85))
            theta_1 = m.atan(v_1[1]/v_1[0])
            a_1[0] = (1/mass)*(T*m.cos(theta_1)-(L*m.sin(theta_1)+D*m.cos(theta_1)))
            a_1[1] = (1/mass)*(T*m.sin(theta_1)+L*m.cos(theta_1)-D*m.sin(theta_1)-self.peso_total)
            T = 0
            #Segunda Iteracion:
            x_2[0] = x[0]+0.5*v_1[0]*dt
            x_2[1] = x[1]+0.5*v_1[1]*dt
            v_2[0] = v[0]+0.5*a_1[0]*dt
            v_2[1] = v[1]+0.5*a_1[1]*dt
            for una_helice in self.helices: #loopea a travez de apc
                v_norm = (v_2[0]**2+v_2[1]**2)**0.5
                T = T+una_helice.calcular_fuerza(RPM_lim,densidad,v_norm)
            L = (0.5*densidad*v_norm**2)*CL*(self.area_ala/10)
            D = (0.5*densidad*v_norm**2)*(cd+(CL**2)/(3.141592*8*0.85))
            theta_2 = m.atan(v_2[1]/v_2[0])
            a_2[0] = (1/mass)*(T*m.cos(theta_2)-(L*m.sin(theta_2)+D*m.cos(theta_2)))
            a_2[1] = (1/mass)*(T*m.sin(theta_2)+L*m.cos(theta_2)-D*m.sin(theta_2)-self.peso_total)
            T = 0
            #Tercera Iteracion:
            x_3[0] = x[0]+0.5*v_2[0]*dt
            x_3[1] = x[1]+0.5*v_2[1]*dt
            v_3[0] = v[0]+0.5*a_2[0]*dt
            v_3[1] = v[1]+0.5*a_2[1]*dt
            for una_helice in self.helices: #loopea a travez de apc
                v_norm = (v_3[0]**2+v_3[1]**2)**0.5
                T = T+una_helice.calcular_fuerza(RPM_lim,densidad,v_norm)
            L = (0.5*densidad*v_norm**2)*CL*(self.area_ala/10)
            D = (0.5*densidad*v_norm**2)*(cd+(CL**2)/(3.141592*8*0.85))
            theta_3 = m.atan(v_3[1]/v_3[0])
            a_3[0] = (1/mass)*(T*m.cos(theta_3)-(L*m.sin(theta_3)+D*m.cos(theta_3)))
            a_3[1] = (1/mass)*(T*m.sin(theta_3)+L*m.cos(theta_3)-D*m.sin(theta_3)-self.peso_total)
            T = 0
            #Cuarta Iteracion:
            x_4[0] = x[0]+v_3[0]*dt
            x_4[1] = x[1]+v_3[1]*dt
            v_4[0] = v[0]+a_3[0]*dt
            v_4[1] = v[1]+a_3[1]*dt
            for una_helice in self.helices: #loopea a travez de apc
                v_norm = (v_4[0]**2+v_4[1]**2)**0.5
                T = T+una_helice.calcular_fuerza(RPM_lim,densidad,v_norm)
            L = (0.5*densidad*v_norm**2)*CL*(self.area_ala/10)
            D = (0.5*densidad*v_norm**2)*(cd+(CL**2)/(3.141592*8*0.85))
            theta_4 = m.atan(v_4[1]/v_4[0])
            a_4[0] = (1/mass)*(T*m.cos(theta_4)-(L*m.sin(theta_4)+D*m.cos(theta_4)))
            a_4[1] = (1/mass)*(T*m.sin(theta_4)+L*m.cos(theta_4)-D*m.sin(theta_4)-self.peso_total)
            #Poniendolo Todo junto:
            x[0] = x[0] + (dt/6)*(v_1[0]+2*v_2[0]+2*v_3[0]+v_4[0])
            x[1] = x[1] + (dt/6)*(v_1[1]+2*v_2[1]+2*v_3[1]+v_4[1])
            v[0] = v[0] + (dt/6)*(a_1[0]+2*a_2[0]+2*a_3[0]+a_4[0])
            v[1] = v[1] + (dt/6)*(a_1[1]+2*a_2[1]+2*a_3[1]+a_4[1])
            i = i + 1
            X.append(x[0])
            Y.append(x[1])
            V.append(v_norm)
            TIME_VECTOR.append(t)
            V_REF.append(V_Stall)
            t = t +dt 
        fig, ax = plt.subplots()
        ax.set_title('Despego o no?')
        ax.set_ylabel('Posicion Vertical (m)')
        ax.set_xlabel(['Posicion Horizontal (m), Velocidad final: ',str(v_norm),' m/s y Stall es ',str(V_Stall),' m/s'])
        ax.plot(X,Y,'--', linewidth=2)
        ax.plot(X,Y_Ground,'--', linewidth=2,color='brown')
        ax.grid(True)
        #plt.show()  
        fig2, ax2 = plt.subplots()
        ax2.set_title('Despego o no?')
        ax2.set_ylabel('Velocidad')
        ax2.set_xlabel(['Tiempo: segundos'])
        ax2.plot(TIME_VECTOR,V,'--', linewidth=2)
        ax2.plot(TIME_VECTOR,V_REF,'--', linewidth=2,color='red')
        ax2.grid(True)
        plt.show()  
        return [X,Y]   
escs = []
motores = []
baterias = []
helices = []
propulsores = []
mi_esc = esc(50)
mi_esc_2 = esc(50)
escs.append(mi_esc)
escs.append(mi_esc_2)
mi_motor = motor(500,0,100,6,0.85) #(kv,mass,A,S,E)
mi_motor2 = motor(500,0,100,6,0.85) #(kv,mass,A,S,E)
motores.append(mi_motor)
motores.append(mi_motor2)
mi_bateria = bateria(6,20000)
baterias.append(mi_bateria)
mi_helice = helice(6,13,2,2) #Pitch Diametro Composicion Numero de Aspas
mi_helice2 = helice(6,13,2,2) #Pitch Diametro Composicion Numero de aspas
mi_helice.insertar_curva('PER3_13x6.dat')
mi_helice2.insertar_curva('PER3_13x6.dat')
helices.append(mi_helice)
helices.append(mi_helice2)
mi_propulsor = propulsor('Motor_1.csv',5)
#G = mi_helice.calcular_fuerza(5110,1.225,8)
propulsores.append(mi_propulsor)
#m_payload,m_frame,Warea:
caso_eve = Avion(propulsores,motores,escs,baterias,helices,1,0,49)
print(str(caso_eve.peso_total/9.81))
#CL,vel_lanzamiento,alt_lanzamiento,densidad,usar_helices,angulo_lanzamiento,celdas
[X,Y] = caso_eve.analizar_hand_Launch(0.3, 4.8, 2, 0.938978, 1, 1*3.14159265/180, 6)
a=1