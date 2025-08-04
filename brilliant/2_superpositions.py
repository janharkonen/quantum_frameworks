def qiskit(n : int):
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit.quantum_info import Statevector

    # Create circuit
    qc = QuantumCircuit(3, 3)
    qc.x(2)

    # Get the statevector and print it in a nicer format
    state = Statevector.from_instruction(qc)
    print("\nState vector:")
    for i, amplitude in enumerate(state):
        basis_state = format(i, f'0{3}b')  # Convert to 3-bit binary
        print(f"|{basis_state}⟩: {amplitude:.4f}")





    qc.measure(0, 0)  # Specify both qubit and classical bit
    qc.measure(1, 1)  # Specify both qubit and classical bit
    qc.measure(2, 2)  # Specify both qubit and classical bit
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
    import cirq
    q0 = cirq.NamedQubit('test0')
    q1 = cirq.NamedQubit('test1')
    q2 = cirq.NamedQubit('test2')
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.H(q1))
    circuit.append(cirq.H(q2))
    # Qubit starts in |0⟩ state
    # Add measurement
    circuit.append(cirq.measure(q0, key='result0'))
    circuit.append(cirq.measure(q1, key='result1'))
    circuit.append(cirq.measure(q2, key='result2'))
    print(circuit)
    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    print('Cirq  --------------------------------------')
    print(result.histogram(key='result0'))
    print(result.histogram(key='result1'))
    print(result.histogram(key='result2'))
    print(simulator.simulate(circuit))

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
    #cirq(n)
    #pennylane(n)
            