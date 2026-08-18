import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { listProviders, createOrder, listOrders } from '../api/resources';

export default function Providers() {
  const [providers, setProviders] = useState([]);
  const [bookingId, setBookingId] = useState(null);
  const [pendingProviderIds, setPendingProviderIds] = useState(new Set());
  const navigate = useNavigate();

  const loadPendingOrders = () => {
    listOrders().then((res) => {
      const pending = res.data
        .filter((o) => o.status === 'pending' && o.provider)
        .map((o) => o.provider);
      setPendingProviderIds(new Set(pending));
    });
  };

  useEffect(() => {
    listProviders().then((res) => setProviders(res.data));
    loadPendingOrders();
  }, []);

  const handleBook = async (provider) => {
    if (pendingProviderIds.has(provider.id)) {
      alert('You already have a pending booking with this provider. Check your Orders page.');
      return;
    }
    if (!window.confirm(`Book ${provider.name} for ¥5000?`)) {
      return;
    }
    setBookingId(provider.id);
    try {
      await createOrder({
        provider: provider.id,
        description: `Booking with ${provider.name}`,
        amount_jpy: 5000,
      });
      navigate('/orders');
    } catch (err) {
      console.error(err);
      alert('Could not create order. Please try again.');
    } finally {
      setBookingId(null);
    }
  };

  return (
    <div>
      <h1>Trusted Providers</h1>
      {providers.map((p) => {
        const alreadyPending = pendingProviderIds.has(p.id);
        return (
          <div key={p.id} style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16, marginBottom: 12 }}>
            <h3>{p.name} {p.is_verified && <span style={{ color: 'green' }}>✔ Verified</span>}</h3>
            <p>{p.category} — {p.location}</p>
            <p>{p.description}</p>
            <p>Languages: {p.languages_spoken}</p>
            <p>Avg rating: {p.average_rating ?? 'No reviews yet'}</p>
            <button onClick={() => handleBook(p)} disabled={bookingId === p.id || alreadyPending}>
              {alreadyPending ? 'Booking pending' : bookingId === p.id ? 'Booking...' : 'Book this provider'}
            </button>
          </div>
        );
      })}
    </div>
  );
}
