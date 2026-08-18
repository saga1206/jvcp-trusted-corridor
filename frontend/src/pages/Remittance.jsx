import { useEffect, useState } from 'react';
import { getRemittanceQuote, listRemittances, createRemittance } from '../api/resources';

export default function Remittance() {
  const [transfers, setTransfers] = useState([]);
  const [form, setForm] = useState({ direction: 'jp_to_vn', send_amount: '', recipient_name: '', recipient_account_ref: '' });
  const [quote, setQuote] = useState(null);

  const load = () => listRemittances().then((res) => setTransfers(res.data));
  useEffect(() => { load(); }, []);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleQuote = async () => {
    if (!form.send_amount) return;
    const res = await getRemittanceQuote({ direction: form.direction, send_amount: form.send_amount });
    setQuote(res.data);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    await createRemittance(form);
    setForm({ ...form, send_amount: '', recipient_name: '', recipient_account_ref: '' });
    setQuote(null);
    load();
  };

  return (
    <div>
      <h1>Cross-Border Remittance</h1>
      <p style={{ marginBottom: '1.5rem' }}>
        <em>Simulation only — not connected to real banking infrastructure.</em>
      </p>

      <div className="card">
        <h2>Send money</h2>
        <form onSubmit={handleSend} style={{ display: 'grid', gap: 8, maxWidth: 400 }}>
          <select name="direction" value={form.direction} onChange={handleChange}>
            <option value="jp_to_vn">Japan → Vietnam</option>
            <option value="vn_to_jp">Vietnam → Japan</option>
          </select>
          <input name="send_amount" type="number" placeholder="Amount to send" value={form.send_amount} onChange={handleChange} required />
          <button type="button" className="btn-primary" onClick={handleQuote}>Get quote</button>

          {quote && (
            <div className="card" style={{ background: 'var(--cream-deep)' }}>
              <p className="mono">Rate: 1 {quote.send_currency} = {quote.exchange_rate} {quote.receive_currency}</p>
              <p className="mono">Fee: {quote.service_fee} {quote.send_currency}</p>
              <p className="mono">Recipient gets: {quote.receive_amount} {quote.receive_currency}</p>
            </div>
          )}

          <input name="recipient_name" placeholder="Recipient name" value={form.recipient_name} onChange={handleChange} required />
          <input name="recipient_account_ref" placeholder="Recipient account reference (mock)" value={form.recipient_account_ref} onChange={handleChange} required />
          <button type="submit" disabled={!quote}>Send transfer</button>
        </form>
      </div>

      <h2 style={{ marginTop: '2rem' }}>Transfer history</h2>
      {transfers.map((t) => (
        <div key={t.id} className="card">
          <p><strong>{t.direction === 'jp_to_vn' ? 'Japan → Vietnam' : 'Vietnam → Japan'}</strong> to {t.recipient_name}</p>
          <p className="mono">{t.send_amount} {t.send_currency} → {t.receive_amount} {t.receive_currency}</p>
          <p>Status: <strong>{t.status}</strong></p>
          <p className="mono">{t.transaction_id}</p>
        </div>
      ))}
      {transfers.length === 0 && <p>No transfers yet.</p>}
    </div>
  );
}