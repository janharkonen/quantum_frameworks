import numpy as np

def qiskit():
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit.quantum_info import Statevector
    from qiskit import __version__
    print(__version__)
    import matplotlib.pyplot as plt

    def energy(angles, n):
        weights = np.array([2, 1, 3, 1, 1]) # weights
        qc = QuantumCircuit(5, 5)
        qc.rx(angles[0], 0)
        qc.rx(angles[1], 1)
        qc.rx(angles[2], 2)
        qc.rx(angles[3], 3)
        qc.rx(angles[4], 4)
        #qc.rx(0, 0)
        qc.barrier()
        #print(qc.draw())

        # Print the state vector
        # state = Statevector.from_instruction(qc)
        #print("\nState vector:")
        #for i, amplitude in enumerate(state):
        #    basis_state = format(i, f'0{qc.num_qubits}b')  # Convert to binary
        #    print(f"|{basis_state}⟩: {amplitude:.4f}")

        qc.measure(0, 0)  # Specify both qubit and classical bit
        qc.measure(1, 1)  # Specify both qubit and classical bit
        qc.measure(2, 2)  # Specify both qubit and classical bit
        qc.measure(3, 3)  # Specify both qubit and classical bit
        qc.measure(4, 4)  # Specify both qubit and classical bit

        simulator = AerSimulator()
        job = simulator.run(qc, shots=n)
        result = job.result()
        counts = result.get_counts()
        #print(counts)
        res = 0
        
        energy_value = 0
        for state, count in counts.items():
            binary_state = []
            for i in state[::-1]:
                binary_state.append(int(i))
            #energy_value += (-np.dot(binary_state, values) + 100*np.square((np.dot(binary_state, weights) - max_weight)))* count
            energy_value += (-np.dot(binary_state, weights))*count
            
        res = energy_value / n
        return res


    def gradient_calc(angles, n: int, delta: float):
        angles_delta0 = angles.copy()
        angles_delta1 = angles.copy()
        angles_delta2 = angles.copy()
        angles_delta3 = angles.copy()
        angles_delta4 = angles.copy()
        angles_delta0[0] = angles[0] + delta
        angles_delta1[1] = angles[1] + delta
        angles_delta2[2] = angles[2] + delta
        angles_delta3[3] = angles[3] + delta
        angles_delta4[4] = angles[4] + delta
        energy_0 = energy(angles, n)
        energy_delta0 = energy(angles_delta0, n)
        energy_delta1 = energy(angles_delta1, n)
        energy_delta2 = energy(angles_delta2, n)
        energy_delta3 = energy(angles_delta3, n)
        energy_delta4 = energy(angles_delta4, n)
        gradient_0 = (energy_delta0 - energy_0)
        gradient_1 = (energy_delta1 - energy_0)
        gradient_2 = (energy_delta2 - energy_0)
        gradient_3 = (energy_delta3 - energy_0)
        gradient_4 = (energy_delta4 - energy_0)
        return energy_0, np.array([gradient_0, gradient_1, gradient_2, gradient_3, gradient_4])/delta

    gradient_delta = 0.01
    gradient_coefficient = 10
    n = 100000
    angles_guess_initial = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    energy_initial, gradient_initial = gradient_calc(angles_guess_initial, n, gradient_delta) 
    
    gradient_old = gradient_initial
    energy_old = energy_initial
    angles_guess_old = angles_guess_initial
    while True:
        print('gradient_delta = ', gradient_delta)
        print('gradient_coefficient = ', gradient_coefficient)
        print('gradient_old = ', gradient_old)
        print('energy_old = ', energy_old)
        print('angles_guess_old = ', angles_guess_old)
        # make new guess and calc the energy and its gradient
        angles_guess_new = angles_guess_old - gradient_coefficient*gradient_old
        print('angles_guess_new = ', angles_guess_new)
        print('angles as binary = ', angles_to_binary(angles_guess_new))
        energy_new, gradient_new = gradient_calc(angles_guess_new, n, gradient_delta)
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
    #cirq(n)
    #pennylane(n)
            