// ResultDisplay.js
import React from 'react';

const ResultDisplay = ({ result, driverName, cutoff }) => {
  if (result.error) {
    return <div className="error">Error: {result.error}</div>;
  }

  const probabilityPercentage = (result.probability * 100).toFixed(1);

  return (
    <div className="result">
      <h2>
        The probability that {driverName} finishes in the top {cutoff} is
      </h2>
      <p>{probabilityPercentage}%</p>
    </div>
  );
};

export default ResultDisplay;
