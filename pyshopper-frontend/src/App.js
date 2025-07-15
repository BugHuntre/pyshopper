import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Login from './Login';
import Dashboard from './Dashboard';
import AdminDashboard from './AdminDashboard';
import Cart from './Cart';
import Wishlist from './Wishlist';
import ManualAdd from './ManualAdd';
import Catalog from './Catalog1';
import Checkout from './Checkout';
import OrderHistory from './OrderHistory';
import ProtectedRoute from './ProtectedRoute';
// import ForgotPassword from './ForgotPassword';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [userData, setUserData] = useState({
    email: localStorage.getItem('email'),
    role: localStorage.getItem('role'),
  });

  useEffect(() => {
    const handleStorageChange = () => {
      setUserData({
        email: localStorage.getItem('email'),
        role: localStorage.getItem('role'),
      });
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const { email, role } = userData;

  return (
    <Router>
      <Routes>
        {/* 🔓 Public Routes */}
        <Route path="/" element={<Login />} />
        

        {/* 🔐 Protected Dashboard */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute allowedRoles={['user', 'admin']}>
              {role === 'admin' ? <AdminDashboard /> : <Dashboard />}
            </ProtectedRoute>
          }
        />

        {/* 🔐 User-only Routes */}
        <Route
          path="/catalog"
          element={
            <ProtectedRoute allowedRoles={['user']}>
              <Catalog />
            </ProtectedRoute>
          }
        />
        <Route
          path="/cart"
          element={
            <ProtectedRoute allowedRoles={['user']}>
              <Cart email={email} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/wishlist"
          element={
            <ProtectedRoute allowedRoles={['user']}>
              <Wishlist email={email} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/manual-add"
          element={
            <ProtectedRoute allowedRoles={['user']}>
              <ManualAdd email={email} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/checkout"
          element={
            <ProtectedRoute allowedRoles={['user']}>
              <Checkout />
            </ProtectedRoute>
          }
        />
        <Route
          path="/orders"
          element={
            <ProtectedRoute allowedRoles={['user']}>
              <OrderHistory />
            </ProtectedRoute>
          }
        />

        {/* 🛑 Fallback Route */}
        <Route path="*" element={<div className="p-4">404: Page Not Found</div>} />
      </Routes>
    </Router>
  );
}

export default App;
