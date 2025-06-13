// frontend/src/components/layout/MainContent.jsx
import React from 'react';
import ConversationDisplay from '../chat/ConversationDisplay.jsx';
import QueryInput from '../chat/QueryInput.jsx';
import '../../styles/Layout.css'; // Pastikan CSS Layout diimpor

const MainContent = ({ conversation, onSendMessage, isProcessing }) => {
  return (
    // Kita gunakan class baru 'main-content-container' untuk flexbox
    <div className="main-content-container">
      <div className="conversation-wrapper">
        <ConversationDisplay conversation={conversation} />
      </div>
      <div className="input-wrapper">
        <QueryInput onSendMessage={onSendMessage} disabled={isProcessing} />
      </div>
    </div>
  );
};

export default MainContent;