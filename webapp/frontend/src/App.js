import React, { useState } from 'react';
import './index.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>NASCAR Prediction App</h1>
      </header>
      <main>
        <DriverPrediction />
        <RaceComparison />
      </main>
    </div>
  );
}

function DriverPrediction() {
  const [driver, setDriver] = useState('');
  const [race, setRace] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(`Driver: ${driver}, Race: ${race}`);
    // Add fetch call to backend API here
  };

  return (
    <section>
      <h2>Predict Driver Finish</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Select Driver:
          <select value={driver} onChange={(e) => setDriver(e.target.value)}>
            <option value="driver1">Driver 1</option>
            <option value="driver2">Driver 2</option>
            <option value="driver3">Driver 3</option>
            {/* Add more drivers here */}
          </select>
        </label>
        <label>
          Select Upcoming Race:
          <select value={race} onChange={(e) => setRace(e.target.value)}>
            <option value="race1">Race 1</option>
            <option value="race2">Race 2</option>
            <option value="race3">Race 3</option>
            {/* Add more races here */}
          </select>
        </label>
        <button type="submit">Get Prediction</button>
      </form>
    </section>
  );
}

function RaceComparison() {
  const [pastRace, setPastRace] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(`Past Race: ${pastRace}`);
    // Add fetch call to backend API here
  };

  return (
    <section>
      <h2>Compare Past Race Results</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Select Past Race:
          <select value={pastRace} onChange={(e) => setPastRace(e.target.value)}>
            <option value="pastRace1">Past Race 1</option>
            <option value="pastRace2">Past Race 2</option>
            <option value="pastRace3">Past Race 3</option>
            {/* Add more past races here */}
          </select>
        </label>
        <button type="submit">Compare Results</button>
      </form>
    </section>
  );
}

export default App;