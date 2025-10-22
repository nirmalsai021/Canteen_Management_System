import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Lottie from 'lottie-react';
import './Register.css';
import foodAnimation from './MwReSvpOcP.json'; // ⬅️ Directly using your existing JSON file

const Register = ({ setUserEmail }) => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    password: '',
    password_confirm: ''
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.password_confirm) {
      alert("❌ Passwords do not match!");
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/users/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (response.status === 201) {
        const data = await response.json();
        alert("✅ Registration Successful!");

        if (setUserEmail) {
          setUserEmail(data.user.email);
        }

        navigate("/login");
      } else {
        const errorData = await response.json();
        alert("❌ Registration failed:\n" + JSON.stringify(errorData, null, 2));
      }
    } catch (error) {
      console.error("Registration error:", error);
      alert("❌ Server error. Please try again later.");
    }
  };

  return (
    <div className="register-container">
      <div className="left-panel">
        <Lottie
          animationData={foodAnimation}
          loop
          autoplay
          style={{ width: '100%', height: '100%' }}
        />
      </div>

      <form className="register-form" onSubmit={handleSubmit}>
        <h2>Create Account</h2>

        <input
          type="text"
          name="first_name"
          placeholder="First Name"
          value={formData.first_name}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="last_name"
          placeholder="Last Name"
          value={formData.last_name}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email Address"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password_confirm"
          placeholder="Confirm Password"
          value={formData.password_confirm}
          onChange={handleChange}
          required
        />
        <button type="submit">SIGN UP</button>
      </form>
    </div>
  );
};

export default Register;
