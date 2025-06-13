// frontend/src/components/details/JsonDisplay.jsx
import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const JsonDisplay = ({ jsonData }) => {
  if (!jsonData || Object.keys(jsonData).length === 0) {
    return <div className="json-placeholder">Tidak ada data JSON untuk ditampilkan.</div>;
  }

  return (
    <SyntaxHighlighter language="json" style={vscDarkPlus} customStyle={{ margin: 0, borderRadius: '5px' }}>
      {JSON.stringify(jsonData, null, 2)}
    </SyntaxHighlighter>
  );
};

export default JsonDisplay;