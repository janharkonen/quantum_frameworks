import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from qiskit import __version__
print(__version__)
import matplotlib.pyplot as plt



def energy(angle, n):
    qc = QuantumCircuit(2, 2)
    qc.x(0)
    qc.rx(-np.pi/2, 0)
    qc.ry(np.pi/2, 1)
    qc.cx(0, 1)
    qc.rz(angle, 1)
    qc.cx(0, 1)
    qc.rx(np.pi/2, 0)
    qc.ry(-np.pi/2, 1)
    qc.barrier()


    print(qc.draw())
    # Print the state vector
    state = Statevector.from_instruction(qc)
    print("\nState vector:")
    for i, amplitude in enumerate(state):
        basis_state = format(i, f'0{qc.num_qubits}b')  # Convert to bin
        probability = (amplitude*amplitude.conjugate()).real
        if probability > 0.0000001:
            print(f"|{basis_state}⟩: {amplitude:.4f}, |P(x)|^2 = {probability:.4f}")
    
    print("\nPolar coordinates state visualisation:")
    for i, amplitude in enumerate(state):
        basis_state = format(i, f'0{qc.num_qubits}b')  # Convert to bin
        vector_length = np.sqrt( (amplitude*amplitude.conjugate()).real )
        if vector_length > 0.0000001:
            angle = np.angle(amplitude)
            angle = angle / (np.pi)
            state_str = f"|{basis_state}⟩: {vector_length:.4f} exp({angle:.4f}*2*pi*i)"
            print(state_str)

    qc.measure(0, 0)
    qc.measure(1, 1)
    simulator = AerSimulator()
    job = simulator.run(qc, shots=n)
    result = job.result()
    counts = result.get_counts()
    #print(counts)
    res = 0
    
    energy_value = 0
    #for state, count in counts.items():
    #    binary_state = []
    #    for i in state[::-1]:
    #        binary_state.append(int(i))
    #    #energy_value += (-np.dot(binary_state, values) + 100*np.square((np.dot(binary_state, weights) - max_weight)))* count
    #    energy_value += count*10000*(1-binary_state[3]-binary_state[4])**2
    #    energy_value += count*10000*(np.dot(binary_state[0:3], weights) - 1*binary_state[3] - 2*binary_state[4])**2
    #    energy_value += count*(-np.dot(binary_state[0:3], values))
        
    return energy_value / n

energy(np.pi*(1-0.0236), 100)
#energy(0.0, 100)

def qiskit():



    def gradient_calc(angle, n: int, delta: float):
        angle_delta = angle.copy() + delta
        energy = energy(angle, n)
        energy_delta = energy(angle_delta, n)
        return energy, (energy_delta - energy)/delta

    gradient_delta = 0.01
    gradient_coefficient = 10 
    n = 100000
    angle_guess_initial = 0.0
    energy_initial, gradient_initial = gradient_calc(angle_guess_initial, n, gradient_delta) 
    
    gradient_old = gradient_initial
    energy_old = energy_initial
    angle_guess_old = angle_guess_initial
    while True:
        if gradient_coefficient > 0.0000001:
            n = 100000
        if gradient_coefficient < 0.0000001:
            n = 1000000
        print('gradient_delta = ', gradient_delta)
        print('gradient_coefficient = ', gradient_coefficient)
        print('gradient_old = ', gradient_old)
        print('energy_old = ', energy_old)
        print('angle_guess_old = ', angle_guess_old)
        # make new guess and calc the energy and its gradient
        angle_guess_new = (angle_guess_old - gradient_coefficient*gradient_old) % (2*np.pi)
        print('angle_guess_new = ', angle_guess_new)
        print('angles as binary = ', angles_to_binary(angle_guess_new))
        energy_new, gradient_new = gradient_calc(angle_guess_new, n, gradient_delta)
        print('energy_new = ', energy_new)
        print('gradient_new = ', gradient_new)
        print('energy_new - energy_old = ', energy_new - energy_old)
        print('--------------------------------')
        # check if new energy is smaller than old energy
        if ((energy_new - energy_old) < 0):
            energy_old = energy_new
            angles_guess_old = angles_guess_new
            gradient_old = gradient_new
            gradient_coefficient = gradient_coefficient * 1.1
        else:
            gradient_coefficient = gradient_coefficient * 0.9
    print('asd')
    #plt.plot(angles, data, 'o')
    #plt.show()

    print('Qiskit  --------------------------------------')

def angles_to_binary(angles):
    binary = []
    for angle in angles:
        value = float((angle/np.pi) % 2)
        if value > 1.5:
            value = value - 2
        binary.append(value)
    return binary

if __name__ == "__main__":
    n = 10000000
    qiskit()
    #print(energy(np.array([0.0, 3.141592, 0.0, 0.0, 3.141592]), 100000))
    #pennylane(n)
            