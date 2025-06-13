// frontend/src/components/chat/ConversationDisplay.jsx
import React from 'react';
import '../../styles/Chat.css';
// Hapus placeholder lama, impor yang baru
import ResultsDisplay from '../results/ResultsDisplay.jsx';
import PlanningPhaseDisplay from './PlanningPhaseDisplay.jsx'; // <-- Pastikan ini ada
import ErrorDisplay from './ErrorDisplay.jsx'; 

// Untuk saat ini, kita definisikan komponen User Query di sini saja
const UserQuery = ({ content }) => (
    <div className="user-query-block">
        <strong>You:</strong> {content}
    </div>
);

const ConversationDisplay = ({ conversation }) => {
  const renderBlock = (block) => {
    switch (block.type) {
      case 'user_query':
        return <UserQuery content={block.content} />;
      
      case 'agent_planning':
        // Gunakan komponen PlanningPhaseDisplay yang sebenarnya
        return <PlanningPhaseDisplay title={block.data.title} steps={block.data.steps} />;
      
      case 'assistant_response':
        return <ResultsDisplay data={block.data} />;
      
      case 'error':
        return <ErrorDisplay errorData={block.data} />;
      
      default:
        return null;
    }
  };

  return (
    <div className="conversation-display">
      {conversation.map((block) => (
        <div key={block.id} className="conversation-block">
          {renderBlock(block)}
        </div>
      ))}
    </div>
  );
};

export default ConversationDisplay;