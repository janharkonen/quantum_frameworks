def qiskit():
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit.quantum_info import Statevector
    from qiskit import __version__
    print(__version__)
    import numpy as np
    import matplotlib.pyplot as plt

    def energy(angles, n):
        j = -1000000
        h = -2000
        qc = QuantumCircuit(3, 3)
        qc.rx(angles[0], 0)
        qc.rx(angles[1], 1)
        qc.rx(angles[2], 2)
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

        simulator = AerSimulator()
        job = simulator.run(qc, shots=n)
        result = job.result()
        counts = result.get_counts()
        #print(counts)
        res = 0
        
        energy_value = 0
        for state, count in counts.items():
            spins = []
            for i in state[::-1]:
                spins.append(2*int(i) - 1)
            j_term = -j * (spins[0]*spins[1] + spins[1]*spins[2])
            h_term = -h * (spins[0] + spins[1] + spins[2])
            energy_value += (j_term + h_term) * count
            
        res = energy_value / n
        return res


    def gradient_direction(angles, n):
        delta = 0.01
        angles_deltax = angles.copy()
        angles_deltay = angles.copy()
        angles_deltaz = angles.copy()
        angles_deltax[0] = angles[0] + delta
        angles_deltay[1] = angles[1] + delta
        angles_deltaz[2] = angles[2] + delta
        energy_0 = energy(angles, n)
        energy_deltax = energy(angles_deltax, n)
        energy_deltay = energy(angles_deltay, n)
        energy_deltaz = energy(angles_deltaz, n)
        gradient_x = (energy_deltax - energy_0) / delta
        gradient_y = (energy_deltay - energy_0) / delta
        gradient_z = (energy_deltaz - energy_0) / delta
        return energy_0, np.array([gradient_x, gradient_y, gradient_z])/np.linalg.norm(np.array([gradient_x, gradient_y, gradient_z]))

    angles_guess = np.array([0.0, 3.0, 3.0])
    energy_old = 10000
    energy_new = 9990
    delta = 0.1
    while (abs(energy_old - energy_new) > energy_old*0.0001):
        if (energy_new > energy_old):
            delta = delta * 0.1
        else:
            delta = delta * 1.1
        energy_old = energy_new
        energy_new, gradient = gradient_direction(angles_guess, 200000)
        print('energy = ', energy_new)
        print('angles = ', angles_guess)
        print('delta = ', delta)
        angles_guess = angles_guess - gradient * delta
    print('asd')
    #plt.plot(angles, data, 'o')
    #plt.show()

    print('Qiskit  --------------------------------------')

if __name__ == "__main__":
    n = 10000000
    qiskit()
    #cirq(n)
    #pennylane(n)
            