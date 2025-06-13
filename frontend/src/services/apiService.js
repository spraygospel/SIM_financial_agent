// frontend/src/services/apiService.js
const BASE_URL = "http://localhost:8000/api/v1";

class ApiService {
    constructor() {
        this.activeEventSource = null;
    }

    async createSession() {
        const response = await fetch(`${BASE_URL}/create_session`, { method: 'POST' });
        if (!response.ok) throw new Error("Gagal membuat sesi.");
        return response.json();
    }

    async submitQuery(sessionId, userQuery) {
        const response = await fetch(`${BASE_URL}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, user_query: userQuery }),
        });
        if (!response.ok) throw new Error("Gagal mengirim query.");
        return response.json();
    }

    listenToStream({ sessionId, onMessage, onError, onOpen }) {
        if (this.activeEventSource) {
            this.activeEventSource.close();
        }

        const url = `${BASE_URL}/stream_updates/${sessionId}`;
        this.activeEventSource = new EventSource(url);

        this.activeEventSource.onopen = () => {
            console.log("Koneksi SSE berhasil dibuka.");
            if (onOpen) onOpen();
        };
        
        this.activeEventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (onMessage) onMessage(data);

                if (data.event_type === "STREAM_END") {
                    this.closeStream();
                }
            } catch (e) {
                console.error("Gagal mem-parsing data SSE:", event.data);
            }
        };

        this.activeEventSource.onerror = (err) => {
            console.error("Error SSE:", err);
            if (onError) onError(err);
            this.closeStream();
        };
    }

    closeStream() {
        if (this.activeEventSource) {
            this.activeEventSource.close();
            this.activeEventSource = null;
            console.log("Koneksi SSE ditutup.");
        }
    }
}

export const apiService = new ApiService();