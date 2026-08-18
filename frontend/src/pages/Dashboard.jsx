import { useEffect, useState } from 'react';
import { getMyProfile } from '../api/resources';

export default function Dashboard() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    getMyProfile().then((res) => setProfile(res.data)).catch(() => {});
  }, []);

  return (
    <div>
      <div className="hero-slider">
        <div className="hero-slide" style={{ backgroundImage: "url('/images/hero-fuji.jpg')" }} />
        <div className="hero-slide" style={{ backgroundImage: "url('/images/hero-kyoto.jpg')" }} />
        <div className="hero-slide" style={{ backgroundImage: "url('/images/hero-hoian.jpg')" }} />
        <div className="hero-slide" style={{ backgroundImage: "url('/images/hero-halong.jpg')" }} />
        <div className="hero-overlay">
          <div>
            <h1>Japan ⇄ Vietnam</h1>
            <p>One trusted layer for identity, payments, and travel across the corridor.</p>
          </div>
        </div>
      </div>

      <h2>Welcome{profile ? `, ${profile.display_name || 'traveler'}` : ''}</h2>
      <div className="card">
        <span className={`stamp ${profile?.is_verified ? 'stamp--verified' : 'stamp--pending'}`}>
          {profile?.is_verified ? 'Verified' : 'Not yet verified'}
        </span>
        <p style={{ marginTop: '0.75rem' }}>
          Use the nav above to plan a trip, chat with the assistant, browse trusted providers, or manage orders.
        </p>
      </div>
    </div>
  );
}