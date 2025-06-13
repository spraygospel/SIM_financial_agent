// frontend/src/components/results/ResultsDisplay.jsx
import React from 'react';
import ExecutiveSummary from './ExecutiveSummary.jsx';
import AnalysisNarrative from './AnalysisNarrative.jsx';
import DataQualityPanel from './DataQualityPanel.jsx';
import '../../styles/Results.css'; // Impor CSS

const ResultsDisplay = ({ data }) => {
  if (!data) return null;

  const { executive_summary, final_narrative, data_quality_score, warnings_for_display } = data;

  // Cek apakah ini respons data yang lengkap atau hanya narasi sederhana
  const isDataReport = executive_summary && executive_summary.length > 0;

  return (
    <div className={`results-display ${isDataReport ? 'data-report' : 'narrative-only'}`}>
      {isDataReport && <ExecutiveSummary summaryItems={executive_summary} />}
      
      <AnalysisNarrative narrative={final_narrative || "Tidak ada respons."} />
      
      {isDataReport && <DataQualityPanel score={data_quality_score} warnings={warnings_for_display} />}
    </div>
  );
};

export default ResultsDisplay;