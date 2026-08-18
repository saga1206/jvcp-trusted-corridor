import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { login, register, googleLogin } from '../api/client';

export default function Login() {
  const [mode, setMode] = useState('login');
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
  e.preventDefault();

  if (loading) return;

  setError('');
  setLoading(true);

  try {
    if (mode === 'login') {
      await login(username, password);
      navigate('/');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    await register(username, email, password, confirmPassword);

    setError(
      'Account created. Please check your email to verify your account.'
    );
  } catch (err) {
    const data = err.response?.data;

    const message =
      data?.detail ||
      data?.error ||
      data?.email?.[0] ||
      data?.username?.[0] ||
      data?.password?.[0] ||
      data?.confirm_password?.[0] ||
      'Something went wrong.';

    setError(message);
  } finally {
    setLoading(false);
  }
};

  const handleGoogleSuccess = async (credentialResponse) => {
    setError('');

    try {
      await googleLogin(credentialResponse.credential);
      navigate('/');
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Google login failed.'
      );
    }
  };

  return (
    <div style={{ maxWidth: 380, margin: '4rem auto', textAlign: 'center' }}>
      <div className="stamp stamp--verified" style={{ marginBottom: '1.5rem' }}>
        Trusted Corridor
      </div>

      <h1 style={{ marginBottom: '0.25rem' }}>Japan ⇄ Vietnam</h1>

      <p style={{ marginBottom: '2rem' }}>
        Digital identity, payments, and trust for both sides of the corridor.
      </p>

      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem' }}>
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={() => setError('Google login failed.')}
        />
      </div>

      <div style={{ margin: '1rem 0' }}>OR</div>

      <form
        onSubmit={handleSubmit}
        style={{ textAlign: 'left', display: 'grid', gap: '0.75rem' }}
      >
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        {mode === 'register' && (
          <input
  placeholder="Email"
  type="text"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  required
/>
        )}

        <input
          placeholder="Password"
          type={showPassword ? 'text' : 'password'}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {mode === 'register' && (
  <input
    placeholder="Confirm Password"
    type={showPassword ? 'text' : 'password'}
    value={confirmPassword}
    onChange={(e) => setConfirmPassword(e.target.value)}
    required
  />
)}

{mode === 'register' && (
  <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
    <input
      type="checkbox"
      checked={showPassword}
      onChange={(e) => setShowPassword(e.target.checked)}
    />
    Show password
  </label>
)}

        {error && (
          <p style={{ color: 'var(--sun-red)', fontSize: '0.85rem', margin: 0 }}>
            {error}
          </p>
        )}

        <button type="submit" disabled={loading}>
  {loading
    ? 'Please wait...'
    : mode === 'login'
      ? 'Log in'
      : 'Create account'}
</button>
      </form>

      <button
        type="button"
        onClick={() => {
          setMode(mode === 'login' ? 'register' : 'login');
          setError(''); setConfirmPassword('');
        }}
        style={{ marginTop: '1rem' }}
      >
        {mode === 'login'
          ? 'Create a new account'
          : 'Already have an account? Log in'}
      </button>
    </div>
  );
}