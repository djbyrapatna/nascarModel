// src/App.js
import React, { useState } from 'react';
import Header from './components/Header';
import ModelForm from './components/ModelForm';
import ResultDisplay from './components/ResultDisplay';

const App = () => {
  const [result, setResult] = useState(null);

  return (
    <div className="App">
      <Header />
      <ModelForm onResult={setResult} />
      {result && <ResultDisplay result={result} />}
    </div>
  );
};

export default App;
