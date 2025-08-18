import React from 'react';
import './Home.css';
import { Player } from '@lottiefiles/react-lottie-player';
import { Link } from 'react-router-dom'; // ✅ import Link
import noodlesAnimation from '../../assets/animations/noodles.json';

const Home = () => {
  return (
    <div className="home-container">
      <div className="overlay-content">
        {/* Text Section */}
        <div className="text-section">
          <h1 className="welcome">Welcome to</h1>
          <h1 className="title">MITS <span>Canteen</span></h1>
          <p className="description">
            Experience the taste of tradition and technology.  
            Order your meals online, reserve your table, and track your orders — all in one place.
          </p>
          <div className="cta-buttons">
            <Link to="/menu">
              <button className="btn orange">Check Menu</button>
            </Link>
          </div>
        </div>

        {/* Right: Only Noodles Lottie Animation */}
        <div className="image-section">
          <Player
            autoplay
            loop
            src={noodlesAnimation}
            style={{ height: '300px', width: '300px' }}
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
