// src/components/ProtectedRoute.js
import React from 'react';
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children, allowedRoles }) {
  const isLoggedIn = localStorage.getItem('logged_in') === 'true';
  const role = localStorage.getItem('role');

  if (!isLoggedIn || !allowedRoles.includes(role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}

export default ProtectedRoute;
