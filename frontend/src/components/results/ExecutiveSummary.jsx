// frontend/src/components/results/ExecutiveSummary.jsx
import React from 'react';
import '../../styles/Results.css';

const ExecutiveSummary = ({ summaryItems }) => {
  if (!summaryItems || summaryItems.length === 0) {
    return null;
  }

  return (
    <div className="executive-summary">
      {summaryItems.map((item, index) => (
        <div key={index} className="summary-item">
          <div className="summary-value">{item.value}</div>
          <div className="summary-label">{item.label}</div>
        </div>
      ))}
    </div>
  );
};

export default ExecutiveSummary;