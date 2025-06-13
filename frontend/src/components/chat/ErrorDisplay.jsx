// frontend/src/components/chat/ErrorDisplay.jsx
import React from 'react';
import '../../styles/Chat.css';

const ErrorDisplay = ({ errorData }) => {
  // Sediakan pesan default jika tidak ada
  const message = errorData?.user_message || "Terjadi kesalahan yang tidak diketahui.";

  return (
    <div className="error-display-block">
      <div className="error-icon">
        ⚠️
      </div>
      <div className="error-content">
        <p className="error-title">Maaf, terjadi kesalahan</p>
        <p className="error-message">{message}</p>
      </div>
    </div>
  );
};

export default ErrorDisplay;