// ResultDisplay.js
import React from 'react';

const ResultDisplay = ({ result, driverName, cutoff }) => {
  if (result.error) {
    return <div className="error">Error: {result.error}</div>;
  }

  const probabilityPercentage = (result.probability * 100).toFixed(1);

  // Function to convert percentage to American betting odds
  const convertToOdds = (percent) => {
    if (percent < 50) {
      const odds = (100 / (percent / 100)) - 100;
      return `+${odds.toFixed(0)}`;
    } else if (percent > 50) {
      const odds = percent / (1 - (percent / 100));
      return `-${odds.toFixed(0)}`;
    } else {
      return "-100";
    }
  };

  const bettingOdds = convertToOdds(probabilityPercentage);

  return (
    <div className="result">
      <h2>
        The probability that {driverName} finishes in the top {cutoff} is
      </h2>
      <h3>{probabilityPercentage}%</h3>
      <h3>Betting Odds: {bettingOdds}</h3>
      <p>If you find higher odds than the above, this is a good bet</p>
    </div>
  );
};

export default ResultDisplay;
