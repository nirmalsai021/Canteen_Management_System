import React, { useState } from "react";
import "./ForgotPassword.css";

const ForgotPassword = () => {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      setMessage("❌ Passwords do not match");
      return;
    }

    setMessage("✅ Password changed successfully!");
    setNewPassword("");
    setConfirmPassword("");
  };

  return (
    <div className="forgot-password-container">
      <h2>Change Password</h2>
      <form onSubmit={handleSubmit} className="forgot-password-form">
        <label>New password:</label>
        <div className="password-input-wrapper">
          <input
            type={showNewPassword ? "text" : "password"}
            placeholder="Enter new password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
          <span
            className="toggle-eye"
            onClick={() => setShowNewPassword((prev) => !prev)}
            title={showNewPassword ? "Hide password" : "Show password"}
          >
            {showNewPassword ? "🔒" : "👁"}
          </span>
        </div>

        <label>Confirm password:</label>
        <div className="password-input-wrapper">
          <input
            type={showConfirmPassword ? "text" : "password"}
            placeholder="Re-enter new password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
          <span
            className="toggle-eye"
            onClick={() => setShowConfirmPassword((prev) => !prev)}
            title={showConfirmPassword ? "Hide password" : "Show password"}
          >
            {showConfirmPassword ? "🔒" : "👁"}
          </span>
        </div>

        <button type="submit">Change Password</button>

        {message && <p className="message">{message}</p>}
      </form>
    </div>
  );
};

export default ForgotPassword;