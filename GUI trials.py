# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 15:16:43 2021

@author: mikva
"""
import PySimpleGUI as sg
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import QuantumCircuit as qc

qubits = 3

circuit = qc.QuantumCircuit(qubits)


layout = [
    [sg.Button("x"), sg.Button("y"), sg.Button("z"), sg.Button("cnot"), sg.Button("ccnot")]
    ]

def updateGates():
    gate_matrix = []
    for i in range(len(circuit.gates)):
        gate_matrix.append([sg.Text(f"Qubit {i}", size=(6,3))])
        for j, element in enumerate(circuit.gates[i]):
            if type(element)==tuple:
                gate_matrix[i].append(sg.Text(element[0], size=(6,3), auto_size_text=True))
            else:
                gate_matrix[i].append(sg.Text(element))
        gate_matrix[i].append(sg.Button(f"Add to Qubit {i}", size=(6,3)))
    return gate_matrix

layout.append([sg.Frame('Circuit Gates:', updateGates(), key='GATES')])
layout.append([sg.Button("Rt"), sg.Button("cz"), sg.Button("cp"), sg.Button("swap")])


window = sg.Window("Test", layout)

chosen_gate = None

while True:
    event, values = window.read()
    #end if closed
    if event == "x" or event == "y" or event == "z" or event == "Rt":
        chosen_gate = event
        print(chosen_gate, ' chosen')
        
    for i in range(len(circuit.gates)):
        if event == f"Add to Qubit {i}":
            print("adding to qubit")
            circuit.addGate(event,[i])
            updated = updateGates()
            
            window.Element('GATES').update([sg.Frame('Circuit Gates:', updateGates(), key='GATES')])
        
    if event == sg.WIN_CLOSED:
        break
    
window.close()

