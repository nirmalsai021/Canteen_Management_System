import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './EmailVerification.css';

const EmailVerification = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError('Please enter a valid email address');
      return;
    }
    
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/password-reset/send-code/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (response.ok) {
        // Show debug code if available (temporary for testing)
        if (data.debug_code) {
          setMessage(`Code sent to email! Debug code: ${data.debug_code}`);
        } else {
          setMessage('Verification code sent to your email! Redirecting...');
        }
        setTimeout(() => {
          navigate('/reset-password', { state: { email } });
        }, 3000);
      } else {
        if (response.status === 404) {
          setError('No account found with this email address. Please check your email or register first.');
        } else {
          setError(data.error || 'Failed to send verification code');
        }
      }
    } catch (err) {
      setError('Network error. Please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="email-verification-container">
      <div className="email-verification-card">
        <h1>Forgot Password</h1>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
              className="form-input"
            />
          </div>
          
          <button type="submit" disabled={loading} className="primary-btn">
            {loading ? 'Sending...' : 'Send Reset Code'}
          </button>
        </form>
        
        <div className="form-links">
          <button onClick={() => navigate('/login')} className="link-btn">
            Back to Login
          </button>
          <span> | </span>
          <button onClick={() => navigate('/reset-password')} className="link-btn">
            Have a reset code?
          </button>
        </div>
        
        {message && <div className="success-message">{message}</div>}
        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
};

export default EmailVerification;