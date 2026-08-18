import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8001/api/v1';

const client = axios.create({
  baseURL: API_BASE,
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default client;

export async function login(username, password) {
  const res = await axios.post(`${API_BASE}/auth/token/`, {
    username,
    password,
  });

  localStorage.setItem('access_token', res.data.access);
  localStorage.setItem('refresh_token', res.data.refresh);

  return res.data;
}

export async function register(username, email, password, confirmPassword) {
  const res = await axios.post(`${API_BASE}/identity/register/`, {
    username,
    email,
    password,
    confirm_password: confirmPassword,
  });

  return res.data;
}

export async function googleLogin(credential) {
  const res = await axios.post(`${API_BASE}/identity/google/`, {
    credential,
  });

  localStorage.setItem('access_token', res.data.access);
  localStorage.setItem('refresh_token', res.data.refresh);

  return res.data;
}

export function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

export function isLoggedIn() {
  return !!localStorage.getItem('access_token');
}