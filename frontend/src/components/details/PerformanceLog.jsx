// frontend/src/components/details/PerformanceLog.jsx
import React from 'react';
import '../../styles/DetailsPanel.css';

const PerformanceLog = ({ metrics }) => {
  if (!metrics) {
    return <div className="details-placeholder">Metrik performa tidak tersedia.</div>;
  }

  return (
    <ul className="performance-list">
      <li>
        <span>Total Durasi:</span>
        <span>{metrics.total_duration_ms ? `${metrics.total_duration_ms.toFixed(0)} ms` : 'N/A'}</span>
      </li>
      {/* Tambahkan metrik lain jika tersedia di masa depan */}
    </ul>
  );
};

export default PerformanceLog;