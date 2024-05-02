import  numpy as np ;
import quafu ;
from quafu import Task
from quafu import QuantumCircuit ;
from quafu import User  ;
from quafu import simulate
import quafu.elements.element_gates as qeg ;
from quafu.elements import UnitaryDecomposer;
import random;
import pickle ;
import time ;
from quafu.elements.element_gates import U3Gate
from quafu.qfasm.qfasm_parser import QfasmParser;
from quafu.qfasm.exceptions import ParserError;
from qiskit.quantum_info import random_unitary
  
# list all possible chocies :
def pC(circ): circ.plot_circuit("");

def gen(N) : # very native way to get these things done
  circ = QuantumCircuit(N)
  for i in range(N) :
    r_qlist = [i for i in range(N)]  ; random.shuffle(r_qlist);
    q_pairs =  []
    while(len(r_qlist)>1):
      p = [r_qlist.pop() , r_qlist.pop() ];

      UnDec = UnitaryDecomposer(np.matrix(random_unitary(4)) , p );
      UnDec.apply_to_qc(circ) ;
  circ.barrier();
  circ.measure([i for i in range(N)] , cbits =[i for i in range(N)]);
  return circ ;


def lswap(L,i,j) : t = L[i] ;  L[i] = L[j] ; L[j] = t ;  return L ;
#def gen_with_swap(m ,d ) :
#  circ = QuantumCircuit(m) ;
#  order_after_swap = [i for i in range(d) ] ;
#  GATE_LIST
#  for i in range(d) :
#    r_qlist = [ i for i in range(N)] ; random.shuffle(r_qlist) ;


def add_U3(qlisp_ins, circ,  q0 ,th, phi, la) :
  #qlisp_ins.append( (('U' , th , phi , la) , q0) ) ;
  qlisp_ins.append((("Rz" , la) , q0));
  qlisp_ins.append((("Ry" , th) , q0)); 
  qlisp_ins.append((("Rz" , phi) , q0));  

  circ.rz(q0 , la) ; 
  circ.ry(q0 , th) ; 
  circ.rz(q0 , phi) ;

  #circ.rz(q0 , phi) ; 
  #circ.ry(q0 , th) ; 
  #circ.rz(q0, la) ;

def add_CZ(qlisp_ins, circ,  q0 ,q1) :
  qlisp_ins.append(  ('CZ' ,  (q0 ,q1)) ) ;
  circ.cz(q0,q1);


def swap(qlisp_ins, circ, q0 , q1) :
  add_U3(qlisp_ins,circ ,  q1  , -np.pi/2 , 0 ,0 ) ;
  add_CZ(qlisp_ins, circ ,q0 , q1);
  add_U3(qlisp_ins,circ ,  q0  , -np.pi/2 , 0 ,0 ) ;
  add_U3(qlisp_ins,circ ,  q1  , np.pi/2 , 0 ,0 ) ;
  add_CZ(qlisp_ins, circ ,q0 , q1);
  add_U3(qlisp_ins,circ ,  q0  , np.pi/2 , 0 ,0 ) ;
  add_U3(qlisp_ins,circ ,  q1  , -np.pi/2 , 0 ,0 ) ;
  add_CZ(qlisp_ins, circ ,q0 , q1);
  add_U3(qlisp_ins,circ ,  q1  , np.pi/2 , 0 ,0 ) ;







def map_qlisp(C, qmap) :
  Cp = [];
  for ins in C :
    ins1_mapped=None;
    if(type(ins[1]) == int) : ins1_mapped = qmap[ins[1]];
    elif(type(ins[1]) == tuple) : ins1_mapped = ( qmap[ins[1][0]],qmap[ins[1][1]]);
    Cp.append( (ins[0] ,ins1_mapped ) )
  return Cp;

