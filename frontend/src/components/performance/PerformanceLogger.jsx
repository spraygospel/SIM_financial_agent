// frontend/src/components/performance/PerformanceLogger.jsx
import React from 'react';
import '../../styles/Performance.css';

// Terima stopwatch sebagai prop
const PerformanceLogger = ({ stopwatch }) => {
  return (
    <div className="performance-logger">
      <h4>Log Performa</h4>
      <div className="performance-grid">
        <div className="metric-label">Total Durasi</div>
        <div className="metric-value stopwatch">{stopwatch.formattedTime}</div>

        {/* Kita bisa tambahkan metrik lain di sini di masa depan */}
        <div className="metric-label">Panggilan LLM</div>
        <div className="metric-value">N/A</div>

        <div className="metric-label">Eksekusi Tool</div>
        <div className="metric-value">N/A</div>
      </div>
    </div>
  );
};

export default PerformanceLogger;