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

from quark import Task

# 实例化任务管理器
token ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjoieWwiLCJleHAiOjE3MTQ5MTgxNTAuMDc5MTIzfQ.oaZaJ2FHyA6tAHE2cNA9lcf30d7wHOzpGVehPCDTHHw'
tmgr = Task(token)

N = 4  ;  ns = 1024; 

def plot_probabilities(sampling_results, title:Optional[str]=None):
    """
    Plot the probabilities from execute results.
    """
    sampling_results = {k: sampling_results[k] for k in sorted(sampling_results)}
    # sampling_results = {k: sampling_results[k] for k in sorted(sampling_results, key=lambda x: int(x, 2))}
    bitstrs = list(sampling_results.keys())
    bitstrs = [str(i) for i in bitstrs]
    probs = list(sampling_results.values())
    plt.figure(figsize=(6,3))
    plt.bar(range(len(probs)), probs, tick_label = bitstrs)
    plt.xticks(rotation=70)
    plt.ylabel("probabilities")
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.title(title)
    plt.show()
 
def simulation(qc,plot:bool):
    aersim = AerSimulator()
    result_ideal = aersim.run(qc).result()
    counts = result_ideal.get_counts()
    n = len(qc.qubits)
    full_result = {}
    for i in range(2**n):
        full_result[bin(i)[2:].zfill(n)] = 0
    for i in counts.keys():
        full_result[i] = counts[i]
    if plot == True:
        plot_probabilities(full_result)
    return full_result


def simulation_4(qc,plot:bool):
    aersim = AerSimulator()
    result_ideal = aersim.run(qc).result()
    counts_zero = result_ideal.get_counts()

    counts = {}
    for key, value in counts_zero.items():
        # processed_key = key.replace(" 0000", "")
        counts[key] = value
    n = len(qc.qubits)
    full_result = {}
    for i in range(2**n):
        full_result[bin(i)[2:].zfill(n)] = 0
    for i in counts.keys():
        full_result[i] = counts[i]
    if plot == True:
        plot_probabilities(full_result)
    return full_result

def get_ideals(circuits_filename, error):
    with open(circuits_filename, 'r') as file:
        circuits = json.load(file)
    circuits_qiskit = {}
    ideals = {}
    for i in range(len(circuits)):
        circuits_qiskit[i] = qiskitQC.from_qasm_str(circuits[str(i)]['qasm'])
        # circuits_qiskit[i].measure_all()
        circuits_qiskit[i].barrier([0,1,2,3,4])
        circuits_qiskit[i].measure([0,1,2,3,4],[0,1,2,3,4])
        ideals[i] = simulation_4(circuits_qiskit[i], plot = False)
        # ideals[i] =  { k[::-1] : v for k,v in ideals[i].items()} ###一会注释掉
    error_set = set(error)
    ideals_new = {key: value for key, value in ideals.items() if key not in error_set}
    ideals_new = {index: value for index, value in enumerate(ideals_new.values())}
    return ideals_new



################get results#####################
def get_results(results_filename):
    df = pd.read_csv(results_filename,header=None)
    ids = df.iloc[:, 0].tolist()
    nc = len(ids)
    error = []
    results = {}
    for i in range(nc):
        try:
            data = tmgr.result(ids[i])['count']
            data_prime =  { k[::-1] : v for k,v in data.items()}
            results[i] = data_prime
            # results[i] = data
        except:
            error.append(i)
            print(i, ids[i])
    results = {index: value for index, value in enumerate(results.values())}

    return results, error

def get_heavy_outputs(result,ideal):

    def heavy_outputs(ideal: OrderedDict):
        sorted_ideal = OrderedDict(sorted(ideal.items(), key=lambda x: x[1]))
        for _ in range(len(ideal)//2):
            key,value = sorted_ideal.popitem(last=False)
        # nheavies = np.sum(list(sorted_ideal.values()))
        return list(sorted_ideal.keys())

    heavy_ideal = heavy_outputs(ideal)

    def check_threshold(heavy_ideal:list, result:OrderedDict, nshots:int):
        nheavies = 0
        for i in result.keys(): 
            if i in heavy_ideal:
                nheavies += result[i]
        nshots = np.sum(list(result.values()))
        return nheavies/nshots

    return check_threshold(heavy_ideal=heavy_ideal, result=result,nshots=np.sum(list(result.values())))

def plot_qv(heavy_outputs, heavy_outputs_simu, chip):
    median_experiment = np.median(heavy_outputs)
    mean_experiment = np.mean(heavy_outputs)
    mean_simulation = np.mean(heavy_outputs_simu)
    key = 0.66

    bins_ex = np.arange(min(heavy_outputs), max(heavy_outputs) + 1, 0.03) 
    bins_si = np.arange(min(heavy_outputs_simu), max(heavy_outputs_simu) + 1, 0.03) 

    plt.hist(heavy_outputs, bins=bins_ex, color='skyblue', edgecolor='black', alpha=0.8)
    plt.hist(heavy_outputs_simu, bins=bins_si, color='orange', edgecolor='black', alpha=0.8)
    plt.xlabel('heavy output')
    plt.ylabel('times')
    plt.title(f'{chip},{5} qubits, {len(heavy_outputs)} tests')
    plt.axvline(mean_experiment, color='skyblue', linestyle='dashed', linewidth=1, label=f'Mean_experiment = {mean_experiment:.2f}')
    plt.axvline(mean_simulation, color='orange', linestyle='dashed', linewidth=1, label=f'Mean_simulation = {mean_simulation:.2f}')
    # plt.axvline(median_experiment, color='green', linestyle='dashed', linewidth=1, label=f'Median_experiment = {median_experiment:.2f}')

    plt.axvline(key, color='red')
    plt.xlim(0,1)
    plt.legend()
    plt.show()
    plt.savefig(f'{chip}.png')
 



#################读取校正#########################
def find_pos(binary_str):
    pos_0 = []
    pos_1 = []
    for i, bit in enumerate(binary_str):
        if bit == '0':
            pos_0.append(i)
        else:
            pos_1.append(i)
    return pos_0, pos_1

def add_x(qlisp_ins, q):
    qlisp_ins.append(('X', q))

def add_i(qlisp_ins, q):
    qlisp_ins.append(('I', q))
 
from qv_kx import map_qlisp
def read_correct_cir(qmap,n_qubit):
    measures =  [ (("Measure",i) , i ) for i in range(n_qubit)] ; 

    read_circuits  = {i:[] for i in range(2**n_qubit)}

    for i in range(2**n_qubit):
        i_2 = bin(i)[2:].zfill(n_qubit)
        i_pos, x_pos = find_pos(i_2)
        for j in  range(n_qubit):
            if j in i_pos:
                add_i(read_circuits[i], j)
            if j in x_pos:
                add_x(read_circuits[i], j)
        read_circuits[i]=map_qlisp(read_circuits[i] , qmap )
        read_circuits[i] = read_circuits[i] + [ ("Barrier",  tuple([w for w in qmap.values()]))] + map_qlisp( measures ,qmap )
    return read_circuits

def get_read_mat(read_results,n_qubit):
    mat = np.zeros((2**n_qubit, 2**n_qubit), dtype=int)
    for i in range(2**n_qubit):
        for j in range(2**n_qubit):
            try:
                mat[i][j] = read_results[i][bin(j)[2:].zfill(n_qubit)[::-1]]
            except:
                mat[i][j] = 0
            # print(read_results[i][bin(j)[2:].zfill(4)])
    mat = mat/10240
    read_mat = np.linalg.inv(mat) 
    return np.transpose(read_mat)

def read_correct(results, read_mat):
    n = len(results)
    results_mat = np.zeros((2**5, n))
    for i in range(n):
        for j in list(results[0].keys()):
            try:
                results_mat[int(j,2),i] = int(results[i][j])
            except:pass
    after_mat = np.dot(read_mat,results_mat)

    def re(i):
        res = {}  
        for j in range(32):
            res[bin(j)[2:].zfill(5)] = after_mat[j][i]
        return res
    
    results_after = {}
    for c in range(n):
        results_after[str(c)] = re(c)

    return results_after


























































