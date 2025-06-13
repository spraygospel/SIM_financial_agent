// frontend/src/main.jsx 
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx'; // Pastikan path ini benar

// Kita impor CSS global kita di sini agar berlaku di seluruh aplikasi
import './styles/global.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);