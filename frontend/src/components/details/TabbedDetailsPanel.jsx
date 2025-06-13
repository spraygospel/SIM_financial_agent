// frontend/src/components/details/TabbedDetailsPanel.jsx
import React, { useState } from 'react';
import InteractiveDataTable from './InteractiveDataTable.jsx';
import JsonDisplay from './JsonDisplay.jsx';
import PerformanceLog from './PerformanceLog.jsx';
import '../../styles/DetailsPanel.css';

const TabbedDetailsPanel = ({ tableColumns, tableData, jsonData, performanceMetrics }) => {
  const [activeTab, setActiveTab] = useState('data');

  const renderContent = () => {
    switch (activeTab) {
      case 'plan':
        return <JsonDisplay jsonData={jsonData} />;
      // Hapus case 'log'
      case 'data':
      default:
        return <InteractiveDataTable columns={tableColumns} data={tableData} />;
    }
  };

  return (
    <div className="tabbed-details-panel">
      <div className="tab-buttons">
        <button onClick={() => setActiveTab('data')} className={activeTab === 'data' ? 'active' : ''}>Data Mentah</button>
        <button onClick={() => setActiveTab('plan')} className={activeTab === 'plan' ? 'active' : ''}>Rencana Eksekusi</button>
        </div>
      <div className="tab-content">
        {renderContent()}
      </div>
    </div>
  );
};

export default TabbedDetailsPanel;