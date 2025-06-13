// frontend/src/App.jsx
import React, { useState, useEffect, useCallback } from 'react';
import MainLayout from './components/layout/MainLayout.jsx';
import { apiService } from './services/apiService';
import { useStopwatch } from './hooks/useStopwatch.js';

function App() {
    const [sessionId, setSessionId] = useState(null);
    const [status, setStatus] = useState('disconnected');
    const [conversation, setConversation] = useState([]);
    const [isProcessing, setIsProcessing] = useState(false);
    // Tambahkan baris yang hilang ini
    const [activeResult, setActiveResult] = useState(null); 
    const stopwatch = useStopwatch();

    const initialize = useCallback(async () => {
        try {
            setStatus('connecting');
            const data = await apiService.createSession();
            setSessionId(data.session_id);
            setConversation([{ id: Date.now(), type: 'assistant_response', data: { final_narrative: data.greeting_message } }]);
            setStatus('connected');
        } catch (e) {
            setStatus('error');
            console.error("Inisialisasi Gagal:", e);
        }
    }, []);

    useEffect(() => {
        initialize();
        return () => apiService.closeStream();
    }, [initialize]);

    const handleSendMessage = async (message) => {
    if (!sessionId || isProcessing) return;

    setIsProcessing(true);
    stopwatch.reset();
    stopwatch.start();

    const agentResponseId = `agent-${Date.now()}`;

    setConversation(prev => [
        ...prev,
        { id: `user-${Date.now()}`, type: 'user_query', content: message },
        { id: agentResponseId, type: 'agent_planning', data: { title: "Agent is thinking...", steps: [] } }
    ]);

    // Langkah 1: Buka koneksi streaming DULU
    apiService.listenToStream({
        sessionId,
        onMessage: (event) => {
            const time = stopwatch.formattedTime;
            console.log(`[FRONTEND @ ${time}] Menerima Event:`, event);

            if (event.event_type === 'PLANNING_UPDATE') {
                setConversation(prev => prev.map(msg => 
                    msg.id === agentResponseId
                        ? { ...msg, data: { ...msg.data, steps: event.data.steps } }
                        : msg
                ));
            } else if (event.event_type === 'FINAL_RESULT') {
                setConversation(prev => prev.map(msg => 
                    msg.id === agentResponseId ? { ...msg, type: 'assistant_response', data: event.data } : msg
                ));
                setActiveResult(event.data);
            } else if (event.event_type === 'STREAM_END') {
                stopwatch.stop();
                setIsProcessing(false);
            }
        },
        onError: (err) => {
            console.error("SSE Error:", err);
            stopwatch.stop();
            setIsProcessing(false);
        }
    });

    // Beri jeda sangat singkat agar koneksi SSE siap
    await new Promise(resolve => setTimeout(resolve, 50)); 
    
    // Langkah 2: Baru kirim query
    await apiService.submitQuery(sessionId, message);
  };
    if (status === 'connecting') return <div>Menghubungkan ke server...</div>;
    if (status === 'error') return <div>Gagal terhubung. Coba refresh.</div>;

  
    return (
        <div className="App">
      <MainLayout 
        stopwatch={stopwatch}
        conversation={conversation}
        onSendMessage={handleSendMessage}
        isProcessing={isProcessing}
        // Teruskan prop activeResult di sini
        activeResult={activeResult}
      />
    </div>
    );
}
export default App;