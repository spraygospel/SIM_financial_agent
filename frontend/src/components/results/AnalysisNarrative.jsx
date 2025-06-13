// frontend/src/components/results/AnalysisNarrative.jsx
import React from 'react';
import ReactMarkdown from 'react-markdown';
import '../../styles/Results.css';

const AnalysisNarrative = ({ narrative }) => {
  return (
    <div className="analysis-narrative">
      <ReactMarkdown>{narrative}</ReactMarkdown>
    </div>
  );
};

export default AnalysisNarrative;