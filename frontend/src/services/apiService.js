// frontend/src/services/apiService.js

const BASE_URL = "http://localhost:8000/api/v1";

export const apiService = {
  startSession: async () => {
    try {
      const response = await fetch(`${BASE_URL}/session/start`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Gagal memulai sesi:", error);
      return null;
    }
  },

  postQuery: async (sessionId, query) => {
    try {
      const response = await fetch(`${BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          user_query: query,
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Gagal mengirim query:", error);
      return null;
    }
  },
};