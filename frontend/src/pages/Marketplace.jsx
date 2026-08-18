import { useEffect, useState } from 'react';
import { searchMarketplace, getRates } from '../api/resources';

export default function Marketplace() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [rates, setRates] = useState([]);

  const search = () => searchMarketplace({ q: query }).then((res) => setResults(res.data));

  useEffect(() => {
    search();
    getRates().then((res) => setRates(res.data));
  }, []);

  return (
    <div>
      <h1>Cross-Border Marketplace</h1>

      {rates.length > 0 && (
        <div style={{ background: '#f3f4f6', padding: 12, borderRadius: 8, marginBottom: 16 }}>
          {rates.map((r) => (
            <span key={r.id} style={{ marginRight: 16 }}>
              1 {r.base_currency} = {r.rate} {r.target_currency} <em>({r.source})</em>
            </span>
          ))}
        </div>
      )}

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search verified providers..."
          style={{ flex: 1, padding: 8 }} />
        <button onClick={search}>Search</button>
      </div>

      {results.map((p) => (
        <div key={p.id} style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16, marginBottom: 12 }}>
          <h3>{p.name}</h3>
          <p>{p.category} — {p.location}</p>
          <p>{p.description}</p>
        </div>
      ))}
      {results.length === 0 && <p>No verified providers matched.</p>}
    </div>
  );
}