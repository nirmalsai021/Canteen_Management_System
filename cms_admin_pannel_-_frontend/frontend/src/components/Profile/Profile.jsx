import React, { useEffect, useState } from 'react';
import api from '../../api';
import './Profile.css';



const Profile = () => {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);
  const token = localStorage.getItem('access_token');

  const fetchProfile = async () => {
    if (!token) {
      setError('You are not logged in.');
      return;
    }

    try {
      const res = await api.get('/api/users/profile/');

      setUserData(res.data);
    } catch (err) {
      console.error('Profile fetch error:', err);
      if (err.response?.status === 401) {
        setError('Session expired. Please log in again.');
      } else {
        setError('Failed to load profile information.');
      }
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  return (
    <div className="profile-container">
      <div className="profile-card">
        <img
          className="avatar"
          src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMCbr-5T_JJrYpdHFJwA9LImzmZC5ejEjk0B5ywInSJ8_B0565mBLb4UZzLKPJcQ6_O98&usqp=CAU"
          alt="User Avatar"
        />
        <h2 className="username">My Profile</h2>

        {error ? (
          <p className="error-message">{error}</p>
        ) : userData ? (
          <div className="profile-details">
            <p><strong>Full Name:</strong> {userData.user.first_name} {userData.user.last_name}</p>
            <p><strong>Email:</strong> {userData.user.email}</p>
          </div>
        ) : (
          <p>Loading profile...</p>
        )}
      </div>
    </div>
  );
};

export default Profile;
