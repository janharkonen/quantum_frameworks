def qiskit(n : int):
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    # Create circuit
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)  # Specify both qubit and classical bit
    print(qc.draw())
    # Run simulation
    simulator = AerSimulator()
    job = simulator.run(qc, shots=n)
    result = job.result()
    counts = result.get_counts()
    print('Qiskit  --------------------------------------')
    print(counts)
    print(f'n = {n}')

def cirq(n : int):
    # WIP
    import cirq
    qubit = cirq.GridQubit(0, 0)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubit))
    # Qubit starts in |0⟩ state
    # Add measurement
    circuit.append(cirq.measure(qubit, key='result'))

    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    print('Cirq  --------------------------------------')
    print(result.histogram(key='result'))

def pennylane(n: int):
    # WIP
    import pennylane as qml
    dev = qml.device('default.qubit', wires=1, shots=1000)

    @qml.qnode(dev)
    def circuit():
        return qml.sample(wires=0)  # or qml.expval(qml.PauliZ(0)) for expectation

    result = circuit()

if __name__ == "__main__":
    n = 10000
    qiskit(n)
    cirq(n)
    pennylane(n)
            