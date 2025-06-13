// frontend/src/components/results/DataQualityPanel.jsx
import React from 'react';
import '../../styles/Results.css';

const DataQualityPanel = ({ score, warnings }) => {
  const getStars = (score) => {
    const starCount = Math.round(score / 20); // Konversi skor 0-100 ke 0-5 bintang
    return '⭐'.repeat(starCount).padEnd(5, '☆');
  };

  return (
    <div className="data-quality-panel">
      {score && (
        <div className="quality-score">
          Kualitas Data: {score}/100 {getStars(score)}
        </div>
      )}
      {warnings && warnings.map((warning, index) => (
        <div key={index} className="quality-warning">
          ⚠️ {warning}
        </div>
      ))}
    </div>
  );
};

export default DataQualityPanel;