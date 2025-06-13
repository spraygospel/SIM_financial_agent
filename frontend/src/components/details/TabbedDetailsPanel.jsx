// frontend/src/components/details/TabbedDetailsPanel.jsx
import React, { useState } from 'react';
import InteractiveDataTable from './InteractiveDataTable.jsx';
import PerformanceLog from './PerformanceLog.jsx';
import '../../styles/DetailsPanel.css';

const TabbedDetailsPanel = ({ tableColumns, tableData }) => {
  // Karena hanya ada satu tab, kita tidak perlu state lagi
  // const [activeTab, setActiveTab] = useState('data');

  const renderContent = () => {
    return <InteractiveDataTable columns={tableColumns} data={tableData} />;
  };

  return (
    <div className="tabbed-details-panel">
      <div className="tab-buttons">
        <button className="active">Data Mentah</button>
      </div>
      <div className="tab-content">
        {renderContent()}
      </div>
    </div>
  );
};

export default TabbedDetailsPanel;