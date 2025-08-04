def qiskit(n : int):
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit.quantum_info import Statevector
    from qiskit import __version__
    print(__version__)
    import numpy as np


    qc = QuantumCircuit(1, 1)
    qc.rx(np.pi*5/6, 0)
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
    print('Qiskit  --------------------------------------')
    print(counts)
    print(f'n = {n}')
    print(f'res = {res}')

def cirq(n : int):
    pass

def pennylane(n: int):
    pass

if __name__ == "__main__":
    n = 10000000
    qiskit(n)
    #cirq(n)
    #pennylane(n)
            