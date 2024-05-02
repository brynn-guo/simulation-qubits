from qiskit_aer import AerSimulator


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time as time
import random
import json
from importlib import reload; 

from qiskit.circuit.library import QuantumVolume as QuantumVolumeCircuit
from qiskit.quantum_info.random import random_unitary
from qiskit import transpile
from qiskit import qasm2
from qiskit.circuit.library import QuantumVolume as QuantumVolumeCircuit
from qiskit.quantum_info.random import random_unitary
from qiskit import QuantumCircuit as qiskitQC
from typing import Optional
from collections import OrderedDict

import quafu ;
from quafu import Task
from quafu import QuantumCircuit as quafuQC;
from quafu import User  ;
from quafu import simulate
from quark import Task

from qv_kx import rand_SU4, swap


token ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjoieWwiLCJleHAiOjE3MTQ5MTgxNTAuMDc5MTIzfQ.oaZaJ2FHyA6tAHE2cNA9lcf30d7wHOzpGVehPCDTHHw'
tmgr = Task(token)



def QV5_chain(r_num) : 
   ways = []

   if(0 == r_num) : 
      qlist = ((0,1), (2,3))
      ways.append([('su',0,1), ('su',2,3)])

      ways.append([('su',2,3), ('su',0,1)])

   elif(1 == r_num) :
      qlist = ((0,1), (3,4))            
      ways.append([('su',0,1), ('su',3,4)])

      ways.append([('su',3,4), ('su',0,1)])
            
   elif(2 == r_num) : 
      qlist = ((0,1), (2,4)) 
      ways.append([('su',0,1), ('sw',2,3), ('su',3,4)])
      ways.append([('su',0,1), ('sw',3,4), ('su',2,3)])

      ways.append([('sw',2,3), ('su',3,4), ('su',0,1)])
      ways.append([('sw',3,4), ('su',2,3), ('su',0,1)])

   elif(3 == r_num) :
      qlist = ((1,2), (3,4)) 
      ways.append([('su',1,2), ('su',3,4)])

      ways.append([('su',3,4), ('su',1,2)]) 

   elif(4 == r_num) :
      qlist = ((1,2), (0,3)) 
      ways.append([('su',1,2), ('sw',0,1), ('sw',1,2), ('su',2,3)])
      ways.append([('su',1,2), ('sw',2,3), ('sw',1,2), ('su',0,1)])
      ways.append([('su',1,2), ('sw',0,1), ('sw',2,3), ('su',1,2)])

      ways.append([('sw',0,1), ('sw',1,2), ('su',2,3), ('su',1,2)])
      ways.append([('sw',2,3), ('sw',1,2), ('su',0,1), ('su',1,2)])
      ways.append([('su',1,2), ('sw',0,1), ('sw',2,3), ('su',1,2)])

   elif(5 == r_num) :   
      qlist = ((1,2), (0,4))  
      ways.append([('su',1,2), ('sw',0,1), ('sw',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('su',1,2), ('sw',0,1), ('sw',3,4), ('sw',2,3), ('su',1,2)])
      ways.append([('su',1,2), ('sw',0,1), ('sw',1,2), ('sw',3,4), ('su',2,3)])
      ways.append([('su',1,2), ('sw',3,4), ('sw',2,3), ('sw',1,2), ('su',0,1)])

      ways.append([('sw',0,1), ('sw',1,2), ('sw',2,3), ('su',3,4), ('su',1,2)])
      ways.append([('sw',0,1), ('sw',3,4), ('sw',2,3), ('su',1,2), ('su',1,2)])
      ways.append([('sw',0,1), ('sw',1,2), ('sw',3,4), ('su',2,3), ('su',1,2)])
      ways.append([('sw',3,4), ('sw',2,3), ('sw',1,2), ('su',0,1), ('su',1,2)])

   elif(6 == r_num) :
      qlist = ((2,3), (1,4)) 
      ways.append([('su',2,3), ('sw',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('su',2,3), ('sw',1,2), ('sw',3,4), ('su',2,3)])
      ways.append([('su',2,3), ('sw',3,4), ('sw',2,3), ('su',1,2)])

      ways.append([('sw',1,2), ('sw',2,3), ('su',3,4), ('su',2,3)])
      ways.append([('sw',1,2), ('sw',3,4), ('su',2,3), ('su',2,3)])
      ways.append([('sw',3,4), ('sw',2,3), ('su',1,2), ('su',2,3)])

   elif(7 == r_num) :
      qlist = ((2,3), (0,4)) 
      ways.append([('su',2,3), ('sw',0,1), ('sw',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('su',2,3), ('sw',0,1), ('sw',1,2), ('sw',3,4), ('su',2,3)])
      ways.append([('su',2,3), ('sw',0,1), ('sw',3,4), ('sw',2,3), ('su',1,2)])
      ways.append([('su',2,3), ('sw',3,4), ('sw',2,3), ('sw',1,2), ('su',0,1)])

      ways.append([('sw',0,1), ('sw',1,2), ('sw',2,3), ('su',3,4), ('su',2,3)])
      ways.append([('sw',0,1), ('sw',1,2), ('sw',3,4), ('su',2,3), ('su',2,3)])
      ways.append([('sw',0,1), ('sw',3,4), ('sw',2,3), ('su',1,2), ('su',2,3)])
      ways.append([('sw',3,4), ('sw',2,3), ('sw',1,2), ('su',0,1), ('su',2,3)])

   elif(8 == r_num) :
      qlist = ((0,2), (3,4)) 
      ways.append([('su',3,4), ('sw',0,1), ('su',1,2)])
      ways.append([('su',3,4), ('sw',1,2), ('su',0,1)])

      ways.append([('sw',0,1), ('su',1,2), ('su',3,4)])
      ways.append([('sw',1,2), ('su',0,1), ('su',3,4)])

   elif(9 == r_num) :
      qlist = ((0,2), (1,3)) 
      ways.append([('sw',0,1), ('su',1,2), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',0,1), ('su',1,2), ('sw',1,2), ('su',2,3)])
      ways.append([('sw',1,2), ('su  ',0,1), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',1,2), ('su',0,1), ('sw',1,2), ('su',2,3)])     

      ways.append([('sw',2,3), ('su',1,2), ('sw',0,1), ('su',1,2)])
      ways.append([('sw',1,2), ('su',2,3), ('sw',0,1), ('su',1,2)])
      ways.append([('sw',2,3), ('su',1,2), ('sw',1,2), ('su',0,1)])
      ways.append([('sw',1,2), ('su',2,3), ('sw',1,2), ('su',0,1)])   

   elif(10 == r_num) :
      qlist = ((0,2), (1,4)) 
      ways.append([('sw',0,1), ('su',1,2), ('sw',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('sw',0,1), ('su',1,2), ('sw',1,2), ('sw',3,4), ('su',2,3)])
      ways.append([('sw',0,1), ('su',1,2), ('sw',3,4), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',1,2), ('su',0,1), ('sw',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('sw',1,2), ('su',0,1), ('sw',1,2), ('sw',3,4), ('su',2,3)])
      ways.append([('sw',1,2), ('su',0,1), ('sw',3,4), ('sw',2,3), ('su',1,2)])

      ways.append([('sw',1,2), ('sw',2,3), ('su',3,4), ('sw',0,1), ('su',1,2)])
      ways.append([('sw',1,2), ('sw',3,4), ('su',2,3), ('sw',0,1), ('su',1,2)])
      ways.append([('sw',3,4), ('sw',2,3), ('su',1,2), ('sw',0,1), ('su',1,2)])
      ways.append([('sw',1,2), ('sw',2,3), ('su',3,4), ('sw',1,2), ('su',0,1)])
      ways.append([('sw',1,2), ('sw',3,4), ('su',2,3), ('sw',1,2), ('su',0,1)])
      ways.append([('sw',3,4), ('sw',2,3), ('su',1,2), ( 'sw',1,2), ('su',0,1)])

   elif(11 == r_num) :
      qlist = ((0,3), (1,4)) 
      ways.append([('sw',0,1), ('sw',1,2), ('su',2,3), ('sw',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('sw',0,1), ('sw',1,2), ('su',2,3), ('sw',1,2), ('sw',3,4), ('su',2,3)])
      ways.append([('sw',0,1), ('sw',1,2), ('su',2,3), ('sw',3,4), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',0,1), ('sw',2,3), ('su',1,2), ('sw',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('sw',0,1), ('sw',2,3), ('su',1,2), ('sw',1,2), ('sw',3,4), ('su',2,3)])
      ways.append([('sw',0,1), ('sw',2,3), ('su',1,2), ('sw',3,4), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',2,3), ('sw',1,2), ('su',0,1), ('sw',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('sw',2,3), ('sw',1,2), ('su',0,1), ('sw',1,2), ('sw',3,4), ('su',2,3)])
      ways.append([('sw',2,3), ('sw',1,2), ('su',0,1), ('sw',3,4), ('sw',2,3), ('su',1,2)])

      ways.append([('sw',1,2), ('sw',2,3), ('su',3,4), ('sw',0,1), ('sw',1,2), ('su',2,3)])
      ways.append([('sw',1,2), ('sw',3,4), ('su',2,3), ('sw',0,1), ('sw',1,2), ('su',2,3)])
      ways.append([('sw',3,4), ('sw',2,3), ('su',1,2), ('sw',0,1), ('sw',1,2), ('su',2,3)])
      ways.append([('sw',1,2), ('sw',2,3), ('su',3,4), ('sw',0,1), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',1,2), ('sw',3,4), ('su',2,3), ('sw',0,1), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',3,4), ('sw',2,3), ('su',1,2), ('sw',0,1), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',1,2), ('sw',2,3), ('su',3,4), ('sw',2,3), ('sw',1,2), ('su',0,1)])
      ways.append([('sw',1,2), ('sw',3,4), ('su',2,3), ('sw',2,3), ('sw',1,2), ('su',0,1)])
      ways.append([('sw',3,4), ('sw',2,3), ('su',1,2), ('sw',2,3), ('sw',1,2), ('su',0,1)])

   elif(12 == r_num) :
      qlist = ((0,3), (2,4)) 
      ways.append([('sw',0,1), ('sw',1,2), ('su',2,3), ('sw',2,3), ('su',3,4)])
      ways.append([('sw',0,1), ('sw',1,2), ('su',2,3), ('sw',3,4), ('su',2,3)])
      ways.append([('sw',0,1), ('sw',2,3), ('su',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('sw',0,1), ('sw',2,3), ('su',1,2), ('sw',3,4), ('su',2,3)])
      ways.append([('sw',2,3), ('sw',1,2), ('su',0,1), ('sw',2,3), ('su',3,4)])
      ways.append([('sw',2,3), ('sw',1,2), ('su',0,1), ('sw',3,4), ('su',2,3)])

      ways.append([('sw',2,3), ('su',3,4), ('sw',0,1), ('sw',1,2), ('su',2,3)])
      ways.append([('sw',3,4), ('su',2,3), ('sw',0,1), ('sw',1,2), ('su',2,3)])
      ways.append([('sw',2,3), ('su',3,4), ('sw',0,1), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',3,4), ('su',2,3), ('sw',0,1), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',2,3), ('su',3,4), ('sw',2,3), ('sw',1,2), ('su',0,1)])
      ways.append([('sw',3,4), ('su',2,3), ('sw',2,3), ('sw',1,2), ('su',0,1)])

   elif(13 == r_num) :
      qlist = ((0,4), (2,3))  
      ways.append([('su',2,3), ('sw',0,1), ('sw',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('su',2,3), ('sw',0,1), ('sw',1,2), ('sw',3,4), ('su',2,3)])
      ways.append([('su',2,3), ('sw',0,1), ('sw',3,4), ('sw',2,3), ('su',1,2)])
      ways.append([('su',2,3), ('sw',3,4), ('sw',2,3), ('sw',1,2), ('su',0,1)])

      ways.append([('sw',0,1), ('sw',1,2), ('sw',2,3), ('su',3,4), ('su',2,3)])
      ways.append([('sw',0,1), ('sw',1,2), ('sw',3,4), ('su',2,3), ('su',2,3)])
      ways.append([('sw',0,1), ('sw',3,4), ('sw',2,3), ('su',1,2), ('su',2,3)])
      ways.append([('sw',3,4), ('sw',2,3), ('sw',1,2), ('su',0,1), ('su',2,3)])

   elif(14 == r_num) : 
      qlist = ((1,3), (2,4))  
      ways.append([('sw',1,2), ('su',2,3), ('sw',2,3), ('su',3,4)])
      ways.append([('sw',1,2), ('su',2,3), ('sw',3,4), ('su',2,3)])
      ways.append([('sw',2,3), ('su',1,2), ('sw',2,3), ('su',3,4)])
      ways.append([('sw',2,3), ('su',1,2), ('sw',3,4), ('su',2,3)])

      ways.append([('sw',2,3), ('su',3,4), ('sw',1,2), ('su',2,3)])
      ways.append([('sw',3,4), ('su',2,3), ('sw',1,2), ('su',2,3)])
      ways.append([('sw',2,3), ('su',3,4), ('sw',2,3), ('su',1,2)])
      ways.append([('sw',3,4), ('su',2,3), ('sw',2,3), ('su',1,2)])

   return qlist, ways


def generate(r_num):
    circuits = {}
    for i,way in enumerate(QV5_chain(r_num)[1]):
        # print(way)
        circ = quafuQC(5)
        qlisp_ins= []
        for j in way :
            if j[0] == 'RSU4':
                rand_SU4(qlisp_ins,circ, j[1] , j[2])
            if j[0] == 'SWAP':
                swap(qlisp_ins,circ, j[1] , j[2])
        circuits[i] = (circ,qlisp_ins)
        
    return circuits

 
def generate_chain(create_list):
   circ = quafuQC(5)
   qlisp_ins= []
   for j in create_list:
      if j[0] == 'RSU4':
            rand_SU4(qlisp_ins,circ, j[1] , j[2])
      if j[0] == 'SWAP':
            swap(qlisp_ins,circ, j[1] , j[2])

   # circ.barrier([0,1,2,3,4])
   # circ.measure([0,1,2,3,4])
   return qlisp_ins, circ
