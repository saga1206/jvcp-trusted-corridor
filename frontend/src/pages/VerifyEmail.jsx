import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import client from '../api/client';

export default function VerifyEmail() {
  const { token } = useParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('Verifying your email...');

  useEffect(() => {
    client.get(`/identity/verify-email/${token}/`)
      .then((res) => {
        localStorage.setItem('access_token', res.data.access);
        localStorage.setItem('refresh_token', res.data.refresh);
        setStatus('Email verified successfully. Redirecting...');
        setTimeout(() => navigate('/'), 1200);
      })
      .catch(() => {
        setStatus('This verification link is invalid or has already been used.');
      });
  }, [token, navigate]);

  return (
    <div style={{ maxWidth: 500, margin: '6rem auto', textAlign: 'center' }}>
      <h1>{status}</h1>
    </div>
  );
}
