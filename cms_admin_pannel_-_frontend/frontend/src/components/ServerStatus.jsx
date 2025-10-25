import React, { useState, useEffect } from 'react';
import api from '../api';

const ServerStatus = () => {
  const [status, setStatus] = useState('checking');
  const [responseTime, setResponseTime] = useState(null);

  useEffect(() => {
    const checkServer = async () => {
      const start = Date.now();
      try {
        await api.get('/api/menu/customer/');
        const time = Date.now() - start;
        setResponseTime(time);
        setStatus(time > 5000 ? 'slow' : 'fast');
      } catch (error) {
        setStatus('down');
      }
    };

    checkServer();
  }, []);

  const getStatusColor = () => {
    switch (status) {
      case 'fast': return '#4CAF50';
      case 'slow': return '#FF9800';
      case 'down': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'fast': return `Server Ready (${responseTime}ms)`;
      case 'slow': return `Server Warming Up (${responseTime}ms)`;
      case 'down': return 'Server Starting...';
      default: return 'Checking Server...';
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: '10px',
      right: '10px',
      background: 'white',
      padding: '8px 12px',
      borderRadius: '20px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
      fontSize: '12px',
      zIndex: 1000,
      display: 'flex',
      alignItems: 'center',
      gap: '6px'
    }}>
      <div style={{
        width: '8px',
        height: '8px',
        borderRadius: '50%',
        backgroundColor: getStatusColor()
      }}></div>
      {getStatusText()}
    </div>
  );
};

export default ServerStatus;