// frontend/src/components/layout/MainLayout.jsx
import React, { useState } from 'react';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import LeftSidebar from './LeftSidebar.jsx';
import MainContent from './MainContent.jsx';
import RightSidebar from './RightSidebar.jsx';
import '../../styles/Layout.css';

const MainLayout = ({ stopwatch, conversation, onSendMessage, isProcessing, activeResult }) => {
  const [isSidebarMinimized, setIsSidebarMinimized] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarMinimized(!isSidebarMinimized);
  };

  return (
    <div className="main-layout">
      <div className={`left-sidebar-wrapper ${isSidebarMinimized ? 'minimized' : ''}`}>
        <LeftSidebar stopwatch={stopwatch} />
      </div>
      
      <button 
        onClick={toggleSidebar} 
        className="minimize-button"
        style={{ left: isSidebarMinimized ? '-15px' : '245px' }}
      >
        {isSidebarMinimized ? '»' : '«'}
      </button>

      <div className="content-panel-group-wrapper">
        <PanelGroup direction="horizontal">
          <Panel>
            <MainContent 
              conversation={conversation} 
              onSendMessage={onSendMessage}
              isProcessing={isProcessing}
            />
          </Panel>
          <PanelResizeHandle className="resize-handle" />
          <Panel defaultSize={40} minSize={25} collapsible={true}>
            <RightSidebar activeResult={activeResult} />
          </Panel>
        </PanelGroup>
      </div>
    </div>
  );
};

export default MainLayout;