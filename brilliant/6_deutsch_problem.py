def qiskit(n : int):
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit.quantum_info import Statevector
    import numpy as np
    from qiskit.visualization import plot_histogram
    from IPython.display import display
    from qiskit import __version__
    print(__version__)
    
    def deutsch_function(case: int):
        # This function generates a quantum circuit for one of the 4 functions
        # from one bit to one bit

        if case not in [1, 2, 3, 4]:
            raise ValueError("`case` must be 1, 2, 3, or 4.")

        f = QuantumCircuit(2)
        if case in [2, 3]:
            f.cx(0, 1)
        if case in [3, 4]:
            f.x(1)
        return f
   
    def compile_circuit(function: QuantumCircuit):
        # Compiles a circuit for use in Deutsch's algorithm.

        n = function.num_qubits - 1
        qc = QuantumCircuit(n + 1, n)

        qc.x(n)
        qc.h(range(n + 1))

        qc.barrier()
        qc.compose(function, inplace=True)
        qc.barrier()

        qc.h(range(n))
        qc.measure(range(n), range(n))

        return qc 

    qc = compile_circuit(deutsch_function(4))
    print(qc.draw())

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
    n = 10000
    qiskit(n)
    #cirq(n)
    #pennylane(n)
            