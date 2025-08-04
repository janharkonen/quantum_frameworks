

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector


def angle1(y):
    return y*np.pi/4

def angle2(x):
    base = np.pi/8
    return base - x*base*2

def prob_correct(x, y):
    qc = QuantumCircuit(2, 2)
    theta1 = angle1(y)
    theta2 = angle2(x)
    qc.h(0)
    qc.cx(0, 1)
    qc.ry(-2*theta1, 0)
    qc.ry(-2*theta2, 1)
    
    state = Statevector.from_instruction(qc)
    total_prob = 0
    print("\nState vector:")
    for i, amplitude in enumerate(state):
        basis_state = format(i, f'0{qc.num_qubits}b')  # Convert to bin
        probability = (amplitude*amplitude.conjugate()).real
        if probability > 0.0000001:
            if x==0 or y==0:
                if int(basis_state[0])-int(basis_state[1]) == 0:
                    total_prob += probability
            else:
                if int(basis_state[0])-int(basis_state[1]) != 0:
                    total_prob += probability


    print("\nPolar coordinates state visualisation:")
    for i, amplitude in enumerate(state):
        basis_state = format(i, f'0{qc.num_qubits}b')  # Convert to bin
        vector_length = np.sqrt( (amplitude*amplitude.conjugate()).real )
        if vector_length > 0.0000001:
            angle = np.angle(amplitude)
            angle = angle / (np.pi)
            state_str = f"|{basis_state}⟩: {vector_length:.4f} exp({angle:.4f}*2*pi*i)"
            print(state_str)
    print(qc.draw())
    return total_prob

p1 = prob_correct(0, 0)
p2 = prob_correct(0, 1)
p3 = prob_correct(1, 0)
p4 = prob_correct(1, 1)
print(p1, p2, p3, p4)
print((p1+p2+p3+p4)/4)


# Print the state vector