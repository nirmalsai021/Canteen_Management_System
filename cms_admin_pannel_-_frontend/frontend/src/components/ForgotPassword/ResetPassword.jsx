import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import './ResetPassword.css';

const ResetPassword = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState(location.state?.email || '');
  const [code, setCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError('Please enter a valid email address');
      return;
    }
    
    // Validate code
    if (code.length !== 6 || !/^\d{6}$/.test(code)) {
      setError('Please enter a valid 6-digit code');
      return;
    }
    
    // Validate password
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
        setMessage('Password reset successfully! Redirecting...');
        setTimeout(() => navigate('/login'), 1500);
      } else {
        if (response.status === 404) {
          setError('No account found with this email address');
        } else if (data.error?.includes('expired')) {
          setError('Verification code has expired. Please request a new code.');
        } else if (data.error?.includes('Invalid')) {
          setError('Invalid verification code. Please check and try again.');
        } else {
          setError(data.error || 'Failed to reset password');
        }
      }
    } catch (err) {
      setError('Network error. Please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="reset-password-container">
      <div className="reset-password-card">
        <h1>Reset Password</h1>
        
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
          
          <div className="form-group">
            <label>Reset Code</label>
            <input
              type="text"
              placeholder="Enter 6-character code from email"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              maxLength="6"
              required
              disabled={loading}
              className="form-input"
            />
          </div>
          
          <div className="form-group">
            <label>New Password</label>
            <div className="password-input-wrapper">
              <input
                type={showPassword ? "text" : "password"}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                disabled={loading}
                className="form-input"
              />
              <span
                className="password-toggle-icon"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </span>
            </div>
          </div>
          
          <button type="submit" disabled={loading} className="primary-btn">
            {loading ? 'Resetting...' : 'Reset Password'}
          </button>
        </form>
        
        <div className="form-links">
          <button onClick={() => navigate('/login')} className="link-btn">
            Back to Login
          </button>
          <span> | </span>
          <button onClick={() => navigate('/forgot-password')} className="link-btn">
            Resend Code
          </button>
        </div>
        
        {message && <div className="success-message">{message}</div>}
        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
};

export default ResetPassword;