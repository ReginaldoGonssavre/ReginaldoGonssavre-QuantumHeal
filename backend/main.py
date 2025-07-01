from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import numpy as np

# Qiskit Imports for Quantum Chemistry
from qiskit_nature.second_quantization import FermionicOp
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit_nature.mappers.second_quantization import JordanWignerMapper
from qiskit_nature.algorithms import VQEDeploy
from qiskit.algorithms import VQE, optimizers
from qiskit.circuit.library import EfficientSU2
from qiskit.utils import QuantumInstance
from qiskit_aer import AerSimulator

# PySCF for classical electronic structure calculation
from pyscf import gto, scf

# --- Pydantic Models ---
class Molecule(BaseModel):
    name: str
    geometry: list[list[str | float]] # Example: [["H", 0.0, 0.0, 0.0], ["H", 0.0, 0.0, 0.74]]
    basis: str = "sto-3g"
    charge: int = 0
    spin: int = 0

class SimulationResult(BaseModel):
    molecule: Molecule
    status: str
    binding_energy: float | None = None
    message: str
    details: dict | None = None

# --- FastAPI App ---
app = FastAPI(
    title="QuantumHeal API",
    description="API for Quantum Molecular Simulations via AigroQuantumSaaS.",
    version="0.1.0",
)

# --- Quantum Simulation Function ---
async def run_quantum_chemistry_simulation(molecule: Molecule):
    try:
        # 1. Define the molecule using PySCF
        atom_str = " ".join([f"{atom[0]} {atom[1]} {atom[2]} {atom[3]}" for atom in molecule.geometry])
        mol = gto.M(atom=atom_str, basis=molecule.basis, charge=molecule.charge, spin=molecule.spin)
        mol.build()

        # 2. Perform a classical Hartree-Fock calculation (for initial guess and integrals)
        mf = scf.RHF(mol).run()

        # 3. Create an ElectronicStructureProblem from PySCF data
        problem = ElectronicStructureProblem.from_pyscf(mf)

        # 4. Map to Qubit Operators (Jordan-Wigner is a common choice)
        qubit_converter = QubitConverter(JordanWignerMapper())
        qubit_op = qubit_converter.convert(problem.second_q_ops()[0]) # Get the Hamiltonian

        # 5. Define the VQE algorithm components
        # Using AerSimulator for local simulation
        quantum_instance = QuantumInstance(AerSimulator(), shots=1024)

        # Ansatz (variational form) - EfficientSU2 is a good general-purpose choice
        ansatz = EfficientSU2(qubit_op.num_qubits, entanglement="linear", reps=1)

        # Optimizer - SPSA is robust for noisy simulations
        optimizer = optimizers.SPSA(maxiter=100)

        # VQE algorithm
        vqe = VQE(ansatz, optimizer=optimizer, quantum_instance=quantum_instance)

        # 6. Run the VQE calculation
        vqe_result = vqe.compute_minimum_eigenvalue(qubit_op)
        
        # Extract the energy
        binding_energy = vqe_result.eigenvalue.real

        return {
            "status": "COMPLETED",
            "binding_energy": binding_energy,
            "message": "Quantum chemistry simulation completed successfully.",
            "details": {
                "optimizer_evals": vqe_result.optimizer_evals,
                "optimal_parameters": {str(k): float(v) for k, v in vqe_result.optimal_parameters.items()} if vqe_result.optimal_parameters else None,
                "raw_result": str(vqe_result) # Convert to string for JSON serialization
            }
        }

    except Exception as e:
        print(f"Error during quantum simulation: {e}")
        raise HTTPException(status_code=500, detail=f"Quantum simulation failed: {str(e)}")

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the QuantumHeal API"}

@app.post("/simulate", response_model=SimulationResult)
async def run_simulation(molecule: Molecule):
    """
    Accepts a molecule and runs a quantum chemistry simulation to find its binding energy.
    """
    print(f"Received simulation request for: {molecule.name}")
    
    # Run the actual quantum simulation
    simulation_output = await run_quantum_chemistry_simulation(molecule)
    
    print(f"Simulation complete for: {molecule.name}")
    
    return SimulationResult(
        molecule=molecule,
        status=simulation_output["status"],
        binding_energy=simulation_output["binding_energy"],
        message=simulation_output["message"],
        details=simulation_output["details"]
    )