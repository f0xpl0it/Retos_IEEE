# -*- coding: utf-8 -*-
"""
=== GROVER VAULT ===

Run this circuit on your local Qiskit simulator.
The state that occurs with the highest probability is the access key.

Dependencies: pip install qiskit qiskit-aer

Format: IEEE{XXXX}  (4 bits, in the order q3q2q1q0)
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile


def oracle(qc):
    # === VAULT ORACLE - hardcoded ===
    qc.x(0)
    qc.x(2)
    qc.x(3)
    qc.h(3)
    qc.mcx([0, 1, 2], 3)
    qc.h(3)
    qc.x(0)
    qc.x(2)
    qc.x(3)


def diffuser(qc, n):
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))


def grover_vault():
    n = 4
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.barrier()
    for _ in range(3):
        oracle(qc)
        qc.barrier()
        diffuser(qc, n)
        qc.barrier()
    qc.measure_all()
    return qc


if __name__ == "__main__":
    qc = grover_vault()
    sim = AerSimulator()
    t = transpile(qc, sim)
    counts = sim.run(t, shots=2048).result().get_counts()
    print("\n=== VAULT MEASUREMENT RESULTS ===")
    for state, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {state} : {count:4d}")
