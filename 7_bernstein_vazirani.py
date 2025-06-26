def qiskit(n : int):
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit.quantum_info import Statevector
    from qiskit import __version__
    print(__version__)
    

    # Make a Bernstein Vazirani black box such that a is [1, 0, 0, 1]
    qc = QuantumCircuit(5, 5)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.h(3)
    qc.x(4)
    qc.h(4)
    qc.barrier()
    qc.cx(0, 4)
    qc.cx(3, 4)
    qc.barrier()
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.h(3)
    qc.h(4)
    qc.barrier()

    print(qc.draw())

    # Print the state vector
    state = Statevector.from_instruction(qc)
    print("\nState vector:")
    for i, amplitude in enumerate(state):
        basis_state = format(i, f'0{qc.num_qubits}b')  # Convert to binary
        print(f"|{basis_state}⟩: {amplitude:.4f}")

    qc.measure(0, 0)  # Specify both qubit and classical bit
    qc.measure(1, 1)  # Specify both qubit and classical bit
    qc.measure(2, 2)  # Specify both qubit and classical bit
    qc.measure(3, 3)  # Specify both qubit and classical bit
    qc.measure(4, 4)  # Specify both qubit and classical bit

    simulator = AerSimulator()
    job = simulator.run(qc, shots=n)
    result = job.result()
    counts = result.get_counts()
    print('Qiskit  --------------------------------------')
    print(counts)
    print(f'n = {n}')

def cirq(n : int):
    pass

def pennylane(n: int):
    pass

if __name__ == "__main__":
    n = 100000
    qiskit(n)
    #cirq(n)
    #pennylane(n)
            