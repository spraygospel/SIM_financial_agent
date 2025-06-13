// frontend/src/components/layout/RightSidebar.jsx
import React from 'react';
import TabbedDetailsPanel from '../details/TabbedDetailsPanel.jsx';

const RightSidebar = ({ activeResult }) => {
  return (
    <div className="right-sidebar">
      <TabbedDetailsPanel
        tableColumns={activeResult?.data_table_headers || []}
        tableData={activeResult?.data_table_for_display || []}
        jsonData={activeResult?.database_operations_plan || {}}
        performanceMetrics={activeResult?.performance_metrics || {}}
      />
    </div>
  );
};

export default RightSidebar;