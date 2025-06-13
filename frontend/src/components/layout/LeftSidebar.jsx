// frontend/src/components/layout/LeftSidebar.jsx
import React from 'react';
import PerformanceLogger from '../performance/PerformanceLogger.jsx';

// Komponen ini sekarang tidak perlu tahu tentang minimize/maximize
const LeftSidebar = ({ stopwatch }) => {
  return (
    <div className="sidebar-content">
      <PerformanceLogger stopwatch={stopwatch} />
    </div>
  );
};

export default LeftSidebar;