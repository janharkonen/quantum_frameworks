def qiskit():
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit.quantum_info import Statevector
    from qiskit import __version__
    print(__version__)
    import numpy as np
    import matplotlib.pyplot as plt

    def spin_avg(angle, n):

        qc = QuantumCircuit(1, 1)
        qc.rx(angle, 0)
        #qc.rx(0, 0)
        qc.barrier()
        print(qc.draw())

        # Print the state vector
        state = Statevector.from_instruction(qc)
        print("\nState vector:")
        for i, amplitude in enumerate(state):
            basis_state = format(i, f'0{qc.num_qubits}b')  # Convert to binary
            print(f"|{basis_state}⟩: {amplitude:.4f}")

        qc.measure(0, 0)  # Specify both qubit and classical bit

        simulator = AerSimulator()
        job = simulator.run(qc, shots=n)
        result = job.result()
        counts = result.get_counts()
        res = 0
        for m, count in counts.items():
            s = 2*int(m) - 1
            res = res + s*count
        res = res/n
        return res


    pointnum = 100
    data = [0]*pointnum
    angles = np.linspace(0, 2*np.pi, pointnum)
    for i, angle in enumerate(angles):
        data[i] = spin_avg(angle, 1000000)
        print(f'angle = {angle}, res = {data[i]}')
    plt.plot(angles, data, 'o')
    plt.show()

    print('Qiskit  --------------------------------------')

def cirq(n : int):
    pass

def pennylane(n: int):
    pass

if __name__ == "__main__":
    n = 10000000
    qiskit()
    #cirq(n)
    #pennylane(n)
            