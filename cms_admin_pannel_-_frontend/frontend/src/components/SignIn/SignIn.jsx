import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import Lottie from "lottie-react";
import "./SignIn.css";
import kitchenAnimation from "./t8twSqZf0H.json";
import { FaEye, FaEyeSlash } from "react-icons/fa"; // ⬅️ Import icons

const SignIn = ({ setUserEmail, setIsLoggedIn }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false); // ⬅️ State for password toggle
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL || 'https://canteen-backend-bbqk.onrender.com'}/api/users/login/`, {
        username,
        password,
      });

      const { access, refresh, user } = response.data;

      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      localStorage.setItem("user", JSON.stringify(user));
      
      // Clear any old tokens
      localStorage.removeItem("user-token");

      if (setUserEmail) setUserEmail(user.email);
      if (setIsLoggedIn) setIsLoggedIn(true);

      navigate("/");
    } catch (error) {
      alert("❌ Login failed: " + (error.response?.data?.detail || "Check your credentials"));
    }
  };

  return (
    <div className="signin-container">
      <form className="signin-form" onSubmit={handleSubmit}>
        <h2>Sign In</h2>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <div className="password-input-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <span
            className="password-toggle-icon"
            onClick={() => setShowPassword((prev) => !prev)}
            title={showPassword ? "Hide Password" : "Show Password"}
          >
            {showPassword ? <FaEyeSlash /> : <FaEye />}
          </span>
        </div>

        <button type="submit">Sign In</button>

        <Link to="/forgot-password" className="forgot-link">
          Forgot Password?
        </Link>
      </form>

      <div className="right-panel">
        <Lottie
          animationData={kitchenAnimation}
          loop
          autoplay
          style={{ width: "100%", height: "100%" }}
        />
      </div>
    </div>
  );
};

export default SignIn;
