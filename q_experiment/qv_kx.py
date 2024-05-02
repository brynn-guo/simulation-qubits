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
#from qiskit.quantum_info import random_unitary

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


def gate_list(m,d) :
  R = [ ];
  current_order = [ i for i in range(m)] ;
  for i in range(d) :
    R0 = [ ];
    l1 = [ i for i in range(m)] ; random.shuffle(l1) ;
    while(len(l1) > 1 ):
      p = [l1.pop() , l1.pop() ];
      R0.append(p) ;
    R.append(R0) ;
  return R;

def chose2from(L):
  #print(L) ;
  LR = [] ; # all posible tuples
  for ip,i in enumerate(L) :
    for j in L[ip+1:]:
      Lp =  L.copy(); Lp.remove(i) ;  Lp.remove(j) ;
      r_list = chose2from(Lp) ; # rest of the posibilites;  is another list
      if(len(r_list) > 0) : r_proc = [[(i,j)] + r for r in r_list ] ;
      else : r_proc =[[(i,j)]];
      #print(r_proc) ;
      LR+=r_proc ;
  return LR ;

N = 4 ;
W= chose2from([0,1,2,3]) ;
S = set();
for w in W : w.sort();
for w in W : S.add(tuple(w)) ;
L = list(S) ;

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


def con_add_SU4(qlisp_ins , circ , q0 , q1  , rlist)  :
  """
    adding a SU4 by constructoin
    parameters : randoms is a list must contain angular information and exeed size of 15
    by the paper
    https://arxiv.org/pdf/2008.08571.pdf
  """
  r = rlist ;

  add_U3(qlisp_ins, circ, q0 , r[0]  ,r[1] , r[2]);
  add_U3(qlisp_ins, circ, q1 , r[3]  ,r[4] , r[5]);
  add_CZ(qlisp_ins, circ ,q0 , q1);
  add_U3(qlisp_ins ,circ, q0,  r[6] ,  np.pi / 2, np.pi / 2 );
  add_U3(qlisp_ins ,circ, q1,  np.pi/2 ,  np.pi ,  r[7]);
  add_CZ(qlisp_ins, circ ,q0 , q1);
  add_U3(qlisp_ins ,circ, q0,  r[8] ,  np.pi , 3*np.pi / 2);
  add_U3(qlisp_ins ,circ,q1,  np.pi/2 ,  0 ,  np.pi/2);
  add_CZ(qlisp_ins, circ ,q0 , q1);
  add_U3(qlisp_ins ,circ,q0,  r[9] ,  r[10] , r[11])
  add_U3(qlisp_ins ,circ,q1,  r[12],  r[13] , r[14])

def rand_SU4(qlisp_ins, circ , q0 , q1) :
  return con_add_SU4(qlisp_ins,circ, q0, q1 ,np.random.random(15)*2*np.pi ) ;

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


def QV4() :
  circ = QuantumCircuit(4);
  qlisp_ins= [];
  for i in range(1):
    r_num = int(random.random()*0) ;
    if(0 == r_num) : rand_SU4(qlisp_ins,circ, 0 , 1 ); rand_SU4(qlisp_ins,circ, 2 , 3 );
    elif(1 == r_num) : rand_SU4(qlisp_ins,circ, 1 , 2 );swap(qlisp_ins,circ,0,1);swap(qlisp_ins,circ,2,3) ;rand_SU4(qlisp_ins,circ, 1 , 2 );
    elif(2 == r_num) : swap(qlisp_ins,circ, 1,2) ;  rand_SU4(qlisp_ins,circ, 0 , 1) ; rand_SU4(qlisp_ins,circ,2,3);
  return qlisp_ins,circ ;

def QV4_SR(Ra, Rsel):
  circ = QuantumCircuit(4);
  qlisp_ins= [];
  for i in range(1):
    r_num = Rsel.take() ;
    if(0 == r_num) : con_add_SU4(qlisp_ins,circ, 0 , 1 ,Ra.take(15)); con_add_SU4(qlisp_ins,circ, 2 , 3,Ra.take(15) );
    elif(1 == r_num) : con_add_SU4(qlisp_ins,circ, 1 , 2 ,Ra.take(15));swap(qlisp_ins,circ,0,1);swap(qlisp_ins,circ,2,3) ;con_add_SU4(qlisp_ins,circ, 1 , 2,Ra.take(15) );
    elif(2 == r_num) : swap(qlisp_ins,circ, 1,2) ;  con_add_SU4(qlisp_ins,circ, 0 , 1,Ra.take(15)) ; con_add_SU4(qlisp_ins,circ,2,3,Ra.take(15));
  return qlisp_ins,circ ;


from qiskit import QuantumCircuit as qiskitQC

def QV4_R(Ra, Rsel):
  circ = QuantumCircuit(4);
  # circ = qiskitQC(4);
  qlisp_ins= [];
  for i in range(4):
    r_num = Rsel.take() ;
    if(0 == r_num) : con_add_SU4(qlisp_ins,circ, 0 , 1 ,Ra.take(15)); con_add_SU4(qlisp_ins,circ, 2 , 3,Ra.take(15) );
    elif(1 == r_num) : con_add_SU4(qlisp_ins,circ, 1 , 2 ,Ra.take(15));swap(qlisp_ins,circ,0,1);swap(qlisp_ins,circ,2,3) ;con_add_SU4(qlisp_ins,circ, 1 , 2,Ra.take(15) );
    elif(2 == r_num) : swap(qlisp_ins,circ, 1,2) ;  con_add_SU4(qlisp_ins,circ, 0 , 1,Ra.take(15)) ; con_add_SU4(qlisp_ins,circ,2,3,Ra.take(15));
  return qlisp_ins,circ ;



def hstates(N , probs) :
  arg_sort = np.argsort(probs) ;
  heavy_states = arg_sort[2**(N-1):];
  return list(heavy_states);

def map_qlisp(C, qmap) :
  Cp = [];
  for ins in C :
    ins1_mapped=None;
    if(type(ins[1]) == int) : ins1_mapped = qmap[ins[1]];
    elif(type(ins[1]) == tuple) : ins1_mapped = ( qmap[ins[1][0]],qmap[ins[1][1]]);
    Cp.append( (ins[0] ,ins1_mapped ) )
  return Cp;

def to_num(w):
  wp ="";
  for i in range(len(w)):
    if(1==w[i]): wp+="0"
    elif(2==w[i]) : wp+="1";
  return int(wp[::-1] , base = 2 ); 
  #return int(wp , base = 2 ); 
