// src/components/Intro/Intro.jsx
import React, { useEffect, useState } from 'react';
import './Intro.css';
import { motion, AnimatePresence } from 'framer-motion';

const Intro = () => {
  const [progress, setProgress] = useState(0);
  const [exitAnimation, setExitAnimation] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev < 100) return prev + 1;
        clearInterval(interval);
        setTimeout(() => setExitAnimation(true), 800);
        return 100;
      });
    }, 30);

    return () => clearInterval(interval);
  }, []);

  return (
    <AnimatePresence>
      {!exitAnimation && (
        <motion.div
          className="intro-wrapper"
          initial={{ opacity: 1 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <div className="intro-content">
            <motion.img
              src="https://cdn-icons-png.flaticon.com/512/1404/1404945.png"
              alt="Pizza"
              className="pizza-logo"
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
            />
            <motion.h1 className="intro-title">
              MITS Canteen <br />
              <span className="loading-text">Loading...</span>
            </motion.h1>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }}></div>
            </div>
            <div className="progress-percent">{progress}%</div>
          </div>

          <motion.div
            className="curtain curtain-left"
            initial={{ x: 0 }}
            animate={{ x: '-100%' }}
            transition={{ delay: 3.2, duration: 1, ease: 'easeInOut' }}
          />
          <motion.div
            className="curtain curtain-right"
            initial={{ x: 0 }}
            animate={{ x: '100%' }}
            transition={{ delay: 3.2, duration: 1, ease: 'easeInOut' }}
          />
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default Intro;