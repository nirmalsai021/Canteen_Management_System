import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ForgotPassword.css';

const ForgotPassword = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // 1: Email, 2: Code & Password
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSendCode = async (e) => {
    e.preventDefault();
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
        setMessage('Verification code sent to your email!');
        setStep(2);
      } else {
        setError(data.error || 'Failed to send verification code');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/password-reset/verify/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          code,
          new_password: newPassword,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Password reset successfully! You can now login with your new password.');
        setTimeout(() => navigate('/login'), 2000);
      } else {
        setError(data.error || 'Failed to reset password');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-form">
        <h2>Reset Password</h2>
        
        {step === 1 ? (
          <form onSubmit={handleSendCode}>
            <p>Enter your email address to receive a verification code</p>
            
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
            />
            
            <button type="submit" disabled={loading}>
              {loading ? 'Sending...' : 'Send Code'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleResetPassword}>
            <p>Enter the verification code sent to {email}</p>
            
            <input
              type="text"
              placeholder="Enter 6-digit code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              maxLength="6"
              required
              disabled={loading}
            />
            
            <input
              type="password"
              placeholder="New password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              disabled={loading}
            />
            
            <input
              type="password"
              placeholder="Confirm new password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={loading}
            />
            
            <button type="submit" disabled={loading}>
              {loading ? 'Resetting...' : 'Reset Password'}
            </button>
            
            <button 
              type="button" 
              onClick={() => setStep(1)}
              className="back-btn"
              disabled={loading}
            >
              Back to Email
            </button>
          </form>
        )}
        
        {message && <div className="success-message">{message}</div>}
        {error && <div className="error-message">{error}</div>}
        
        <button onClick={() => navigate('/login')} className="cancel-btn">
          Back to Login
        </button>
      </div>
    </div>
  );
};

export default ForgotPassword;