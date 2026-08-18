import { BrowserRouter, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { isLoggedIn, logout } from './api/client';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Identity from './pages/Identity';
import Providers from './pages/Providers';
import Planner from './pages/Planner';
import Assistant from './pages/Assistant';
import Marketplace from './pages/Marketplace';
import Orders from './pages/Orders';
import AdminStats from './pages/AdminStats';
import Remittance from './pages/Remittance';
import VerifyEmail from './pages/VerifyEmail';

function ProtectedRoute({ children }) {
  return isLoggedIn() ? children : <Navigate to="/login" />;
}

function Nav() {
  const navigate = useNavigate();
  if (!isLoggedIn()) return null;
  return (
    <nav className="shell-nav">
      <span className="brand"><span className="brand-mark">印</span>JVCP</span>
      <Link to="/" className="nav-link">Dashboard</Link>
      <Link to="/identity" className="nav-link">Identity</Link>
      <Link to="/providers" className="nav-link">Explore</Link>
      <Link to="/planner" className="nav-link">AI Planner</Link>
      <Link to="/assistant" className="nav-link">Assistant</Link>
      <Link to="/marketplace" className="nav-link">Marketplace</Link>
      <Link to="/orders" className="nav-link">Orders</Link>
      <Link to="/remittance" className="nav-link">Remittance</Link>
      <Link to="/admin" className="nav-link">Admin</Link>
      <button className="btn-logout" onClick={() => { logout(); navigate('/login'); }}>Log out</button>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Nav />
      <div className="page">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/identity" element={<ProtectedRoute><Identity /></ProtectedRoute>} />
          <Route path="/providers" element={<ProtectedRoute><Providers /></ProtectedRoute>} />
          <Route path="/planner" element={<ProtectedRoute><Planner /></ProtectedRoute>} />
          <Route path="/assistant" element={<ProtectedRoute><Assistant /></ProtectedRoute>} />
          <Route path="/marketplace" element={<ProtectedRoute><Marketplace /></ProtectedRoute>} />
          <Route path="/orders" element={<ProtectedRoute><Orders /></ProtectedRoute>} />
          <Route path="/remittance" element={<ProtectedRoute><Remittance /></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute><AdminStats /></ProtectedRoute>} />
          <Route path="/verify-email/:token/" element={<VerifyEmail />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}