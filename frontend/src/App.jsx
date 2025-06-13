// frontend/src/App.jsx

import React, { useState, useEffect, useMemo, useRef } from 'react';
import MainLayout from './components/layout/MainLayout.jsx';
import { apiService } from './services/apiService';
import { useStopwatch } from './hooks/useStopwatch.js';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [conversation, setConversation] = useState([]);
  const [activeResult, setActiveResult] = useState(null);
  const stopwatch = useStopwatch();
  const eventSourceRef = useRef(null);

  useEffect(() => {
    const initializeSession = async () => {
      try {
        const data = await apiService.startSession();
        if (data && data.session_id) {
          setSessionId(data.session_id);
          if (data.greeting_message) {
            setConversation([{
              id: Date.now(), type: 'assistant_response',
              data: { final_narrative: data.greeting_message }
            }]);
          }
        } else {
          throw new Error("Gagal mendapatkan session_id.");
        }
      } catch (err) {
        setError("Tidak dapat terhubung ke server.");
      }
    };
    initializeSession();
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  const handleSendMessage = async (message) => {
    if (!sessionId || isProcessing) return;

    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }
    
    stopwatch.reset();
    stopwatch.start();
    setIsProcessing(true);
    
    const planningBlockId = Date.now() + 1;
    setConversation(prev => [
      ...prev,
      { id: Date.now(), type: 'user_query', content: message },
      { id: planningBlockId, type: 'agent_planning', data: { steps: [] } }
    ]);
    
    await apiService.postQuery(sessionId, message);

    eventSourceRef.current = apiService.listenToStream(
      sessionId,
      (event) => { // onMessage
        if (event.event_type === 'PLANNING_UPDATE') {
          setConversation(prev => prev.map(block => 
            block.id === planningBlockId 
              ? { ...block, data: { steps: event.data.steps } } 
              : block
          ));
        } else if (event.event_type === 'FINAL_RESULT') {
          stopwatch.stop();
          setIsProcessing(false);
          setConversation(prev => prev.map(block => 
            block.id === planningBlockId 
              ? { ...block, type: 'assistant_response', data: event.data } 
              : block
          ));
          setActiveResult(event.data);
          eventSourceRef.current.close();
        } else if (event.event_type === 'WORKFLOW_ERROR') {
          stopwatch.stop();
          setIsProcessing(false);
          setConversation(prev => prev.map(block => 
            block.id === planningBlockId 
              ? { ...block, type: 'error', data: event.data } 
              : block
          ));
          eventSourceRef.current.close();
        }
      },
      (err) => { // onError
        console.error("SSE connection error:", err);
        stopwatch.stop();
        setIsProcessing(false);
      }
    );
  };
  
  const isLoading = !sessionId && !error;

  if (isLoading) return <div style={{ padding: '2rem' }}>Initializing Session...</div>;
  if (error) return <div style={{ padding: '2rem', color: 'red' }}>Error: {error}</div>;

  return (
    <div className="App">
      <MainLayout 
        stopwatch={stopwatch}
        conversation={conversation}
        onSendMessage={handleSendMessage}
        isProcessing={isProcessing}
        activeResult={activeResult}
      />
    </div>
  );
}

export default App;