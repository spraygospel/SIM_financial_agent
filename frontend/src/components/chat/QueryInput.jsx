// frontend/src/components/chat/QueryInput.jsx
import React, { useState } from 'react';
import '../../styles/Chat.css'; // Kita akan buat file CSS ini sebentar lagi

const QueryInput = ({ onSendMessage, disabled }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="query-input-form">
      <input
        type="text"
        className="query-input"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ketik pertanyaan Anda di sini..."
        disabled={disabled}
      />
      <button type="submit" className="send-button" disabled={disabled}>
        Send
      </button>
    </form>
  );
};

export default QueryInput;