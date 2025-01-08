// ResultDisplay.js
import React from 'react';

const ResultDisplay = ({ result }) => {
  if (result.error) {
    return <div className="error">Error: {result.error}</div>;
  }

  return (
    <div className="result">
      <h2>Prediction Result</h2>
      <p>Probability: {result.probability}</p>
    </div>
  );
};

export default ResultDisplay;
