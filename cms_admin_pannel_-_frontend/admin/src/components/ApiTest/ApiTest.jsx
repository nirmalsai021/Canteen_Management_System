import React, { useState } from 'react';

const ApiTest = () => {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const testApi = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/menu/`);
      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      setResult(`Error: ${error.message}`);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h3>API Connection Test</h3>
      <p>Backend URL: {process.env.REACT_APP_API_URL}</p>
      <button onClick={testApi} disabled={loading}>
        {loading ? 'Testing...' : 'Test API Connection'}
      </button>
      <pre style={{ background: '#f5f5f5', padding: '10px', marginTop: '10px' }}>
        {result}
      </pre>
    </div>
  );
};

export default ApiTest;