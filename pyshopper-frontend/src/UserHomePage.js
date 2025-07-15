// src/UserHomePage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

function UserHomePage() {
  const navigate = useNavigate();
  const email = localStorage.getItem('email');

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  return (
    <div className="container text-center py-5">
      <h2 className="mb-4">👋 Welcome to PyShopper!</h2>
      <p className="mb-4"><strong>Logged in as:</strong> {email}</p>

      <div className="d-grid gap-3 col-6 mx-auto">
        <button className="btn btn-outline-primary" onClick={() => navigate('/catalog')}>
          🛍️ Browse Product Catalog
        </button>

        <button className="btn btn-outline-success" onClick={() => navigate('/cart')}>
          🛒 View Your Cart
        </button>

        <button className="btn btn-outline-warning" onClick={() => navigate('/wishlist')}>
          💖 View Wishlist
        </button>

        <button className="btn btn-outline-info" onClick={() => navigate('/manual-add')}>
          ➕ Manually Add to Cart
        </button>

        <button className="btn btn-outline-danger" onClick={handleLogout}>
          🚪 Logout
        </button>
      </div>
    </div>
  );
}

export default UserHomePage;
