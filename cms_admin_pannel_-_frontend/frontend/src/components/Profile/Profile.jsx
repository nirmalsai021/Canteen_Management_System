import React, { useEffect, useState } from 'react';
import api from '../../api';
import './Profile.css';

const Profile = () => {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);
  const token = localStorage.getItem('access_token');

  const refreshAccessToken = async () => {
    const refresh = localStorage.getItem('refresh_token');
    const adminToken = localStorage.getItem('admin-token');
    
    // If admin token exists, don't try to refresh JWT
    if (adminToken) return adminToken;
    
    if (!refresh) return null;

    try {
      const res = await api.post('/api/token/refresh/', { refresh });
      const newAccess = res.data.access;
      localStorage.setItem('access_token', newAccess);
      return newAccess;
    } catch (err) {
      console.error('Token refresh failed:', err);
      return null;
    }
  };

  const fetchProfile = async (accessToken) => {
    try {
      const res = await api.get('/api/users/profile/info/');

      setUserData(res.data);
    } catch (err) {
      if (err.response?.status === 401) {
        const adminToken = localStorage.getItem('admin-token');
        if (adminToken) {
          // Admin token doesn't expire, just retry
          fetchProfile(adminToken);
        } else {
          const newToken = await refreshAccessToken();
          if (newToken) {
            fetchProfile(newToken);
          } else {
            setError('Session expired. Please log in again.');
          }
        }
      } else {
        console.error('Profile fetch error:', err);
        setError('Failed to load profile information.');
      }
    }
  };

  useEffect(() => {
    if (!token) {
      setError('You are not logged in.');
    } else {
      fetchProfile(token);
    }
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
            <p><strong>Username:</strong> {userData.user?.username || 'N/A'}</p>
            <p><strong>Full Name:</strong> {userData.user?.first_name || ''} {userData.user?.last_name || ''}</p>
            <p><strong>Email:</strong> {userData.user?.email || 'N/A'}</p>
            <p><strong>User Type:</strong> {userData.user_type || 'Customer'}</p>
            {userData.profile && (
              <div>
                {userData.profile.roll_number && <p><strong>Roll Number:</strong> {userData.profile.roll_number}</p>}
                {userData.profile.address && <p><strong>Address:</strong> {userData.profile.address}</p>}
              </div>
            )}
          </div>
        ) : (
          <p>Loading profile...</p>
        )}
      </div>
    </div>
  );
};

export default Profile;
