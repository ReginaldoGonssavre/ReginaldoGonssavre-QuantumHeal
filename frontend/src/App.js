import React, { useState } from 'react';
import './App.css';
import axios from 'axios'; // Import axios

function App() {
  const [moleculeName, setMoleculeName] = useState('Hydrogen');
  const [moleculeGeometry, setMoleculeGeometry] = useState('[["H", 0.0, 0.0, 0.0], ["H", 0.0, 0.0, 0.74]]');
  const [simulationResult, setSimulationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setSimulationResult(null);

    try {
      const geometryParsed = JSON.parse(moleculeGeometry);
      const response = await axios.post('http://localhost:8000/simulate', { // Assuming backend runs on port 8000
        name: moleculeName,
        geometry: geometryParsed,
      });
      setSimulationResult(response.data);
    } catch (err) {
      console.error("Error during simulation:", err);
      setError(err.response ? err.response.data.detail : err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>QuantumHeal Simulator</h1>
        <p>Simulate molecular binding energies using quantum algorithms.</p>
      </header>
      <main>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="moleculeName">Molecule Name:</label>
            <input
              type="text"
              id="moleculeName"
              value={moleculeName}
              onChange={(e) => setMoleculeName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="moleculeGeometry">Molecule Geometry (JSON array of [atom, x, y, z]):</label>
            <textarea
              id="moleculeGeometry"
              value={moleculeGeometry}
              onChange={(e) => setMoleculeGeometry(e.target.value)}
              rows="5"
              required
            ></textarea>
            <small>Example: `[["H", 0.0, 0.0, 0.0], ["H", 0.0, 0.0, 0.74]]` for H2</small>
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Simulating...' : 'Run Quantum Simulation'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            <h3>Error:</h3>
            <p>{error}</p>
          </div>
        )}

        {simulationResult && (
          <div className="simulation-results">
            <h2>Simulation Results</h2>
            <p><strong>Molecule:</strong> {simulationResult.molecule.name}</p>
            <p><strong>Status:</strong> {simulationResult.status}</p>
            {simulationResult.binding_energy !== null && (
              <p><strong>Binding Energy:</strong> {simulationResult.binding_energy.toFixed(6)} Hartree</p>
            )}
            <p><strong>Message:</strong> {simulationResult.message}</p>
            {simulationResult.details && (
              <div>
                <h3>Details:</h3>
                <pre>{JSON.stringify(simulationResult.details, null, 2)}</pre>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;