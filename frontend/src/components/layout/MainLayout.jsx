// frontend/src/components/layout/MainLayout.jsx
import React, { useState } from 'react'; // Impor useState
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import LeftSidebar from './LeftSidebar.jsx';
import MainContent from './MainContent.jsx';
import RightSidebar from './RightSidebar.jsx';
import '../../styles/Layout.css';

const MainLayout = ({ stopwatch, conversation, onSendMessage, isProcessing, activeResult }) => {
  // Pindahkan state dan fungsi toggle ke sini
  const [isSidebarMinimized, setIsSidebarMinimized] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarMinimized(!isSidebarMinimized);
  };

  return (
    <div className="main-layout">
      {/* Gunakan state untuk mengubah class CSS */}
      <div className={`left-sidebar-container ${isSidebarMinimized ? 'minimized' : ''}`}>
        <LeftSidebar stopwatch={stopwatch} />
      </div>
      
      {/* Tombol toggle sekarang bagian dari MainLayout */}
      <button onClick={toggleSidebar} className="minimize-button">
        {isSidebarMinimized ? '»' : '«'}
      </button>

      <PanelGroup direction="horizontal">
        {/* Hapus panel kiri dari sini */}
        <Panel>
          <MainContent 
            conversation={conversation} 
            onSendMessage={onSendMessage}
            isProcessing={isProcessing}
          />
        </Panel>
        <PanelResizeHandle className="resize-handle" />
        <Panel defaultSize={30} minSize={20} collapsible={true}>
          <RightSidebar activeResult={activeResult} />
        </Panel>
      </PanelGroup>
    </div>
  );
};

export default MainLayout;