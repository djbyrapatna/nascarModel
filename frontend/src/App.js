// src/App.js
import React, { useState } from 'react';
import Header from './components/Header';
import ModelForm from './components/ModelForm';
import ResultDisplay from './components/ResultDisplay';
import './App.css'; 

const App = () => {
  const [result, setResult] = useState(null);
  const [formData, setFormData] = useState({
    driverName: 'Chase Elliott',
    raceNumber: '20',
    year: '2024',
    modelDesc: '',
    cutoff: ''
  });

  return (
    <div className="App">
      <Header />
      <ModelForm onResult={setResult} formData={formData} setFormData={setFormData} />
      {result && (
        <ResultDisplay
          result={result}
          driverName={formData.driverName}
          cutoff={formData.cutoff}
        />
      )}
    </div>
  );
};

export default App;
