// frontend/src/components/chat/PlanningPhaseDisplay.jsx
import React from 'react';
import '../../styles/PlanningPhase.css'; // CSS khusus untuk komponen ini

const PlanningPhaseDisplay = ({ title, steps }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <div className="status-icon active"></div>; // Lingkaran berdenyut
      case 'completed':
        return <div className="status-icon completed">✅</div>;
      case 'failed':
        return <div className="status-icon failed">❌</div>;
      default: // 'pending'
        return <div className="status-icon pending"></div>;
    }
  };

  return (
    <div className="planning-phase">
      <h4 className="planning-title">🧠 {title || 'Agent is thinking...'}</h4>
      <ul className="planning-steps">
        {steps.map((step, index) => (
          <li key={index} className={`step-item ${step.status}`}>
            {getStatusIcon(step.status)}
            <span className="step-text">{step.step_text}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PlanningPhaseDisplay;