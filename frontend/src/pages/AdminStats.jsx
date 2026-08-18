import { useEffect, useState } from 'react';
import { getAdminDashboard } from '../api/resources';

export default function AdminStats() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    getAdminDashboard().then((res) => setStats(res.data)).catch(() => setError('Admin access required.'));
  }, []);

  if (error) return <p>{error}</p>;
  if (!stats) return <p>Loading...</p>;

  const Section = ({ title, data }) => (
    <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16, marginBottom: 12 }}>
      <h3>{title}</h3>
      {Object.entries(data).map(([k, v]) => (
        <p key={k}>{k}: <strong>{v ?? '—'}</strong></p>
      ))}
    </div>
  );

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <Section title="Acquisition" data={stats.acquisition} />
      <Section title="Engagement" data={stats.engagement} />
      <Section title="Trust" data={stats.trust} />
      <Section title="Commerce" data={stats.commerce} />
    </div>
  );
}