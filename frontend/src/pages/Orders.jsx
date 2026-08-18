import { useEffect, useState } from 'react';
import client from '../api/client';
import { listOrders, requestRefund } from '../api/resources';

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [refundReason, setRefundReason] = useState({});
  const [method, setMethod] = useState({});

  const load = () => listOrders().then((res) => setOrders(res.data));
  useEffect(() => { load(); }, []);

  const handleInitiate = async (id) => {
    await client.post(`/payments/orders/${id}/pay/`, { method: method[id] || 'qr_code' });
    load();
  };
  const handleConfirm = async (id) => {
    await client.post(`/payments/orders/${id}/confirm/`);
    load();
  };
  const handleRefund = async (id) => {
    await requestRefund(id, { reason: refundReason[id] || 'Requested via app', amount_jpy: orders.find(o => o.id === id).amount_jpy });
    load();
  };

  return (
    <div>
      <h1>Orders & Transactions</h1>
      {orders.map((o) => (
        <div key={o.id} className="card">
          <h3>{o.description} — ¥{o.amount_jpy}</h3>
          <p>Status: <strong>{o.status}</strong></p>

          {o.status === 'pending' && (
            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <select onChange={(e) => setMethod({ ...method, [o.id]: e.target.value })} defaultValue="qr_code">
                <option value="qr_code">QR code</option>
                <option value="nfc_tap">NFC tap</option>
                <option value="card_mock">Card (mock)</option>
              </select>
              <button className="btn-primary" onClick={() => handleInitiate(o.id)}>Start payment</button>
            </div>
          )}

          {o.payment && o.payment.status === 'initiated' && (
            <div style={{ marginTop: 12, textAlign: 'center' }}>
              {o.payment.method === 'qr_code' ? (
                <>
                  <img
                    alt="Scan to pay"
                    src={`https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(o.payment.qr_payload)}`}
                  />
                  <p className="mono">{o.payment.transaction_id}</p>
                </>
              ) : (
                <p>Tap to confirm ({o.payment.method.replace('_', ' ')})</p>
              )}
              <button className="btn-primary" onClick={() => handleConfirm(o.id)}>
                {o.payment.method === 'qr_code' ? "I've scanned it" : 'Confirm'}
              </button>
            </div>
          )}

          {o.payment?.status === 'confirmed' && (
            <p className="mono">✓ Paid via {o.payment.method.replace('_', ' ')} — {o.payment.transaction_id}</p>
          )}

          {o.status === 'paid' && o.refunds.length === 0 && (
            <div style={{ marginTop: 8 }}>
              <input placeholder="Refund reason" onChange={(e) => setRefundReason({ ...refundReason, [o.id]: e.target.value })} />
              <button onClick={() => handleRefund(o.id)} style={{ marginLeft: 8 }}>Request refund</button>
            </div>
          )}
          {o.refunds.map((r) => (
            <p key={r.id}>Refund: {r.status} — ¥{r.amount_jpy} ({r.reason})</p>
          ))}
        </div>
      ))}
      {orders.length === 0 && <p>No orders yet.</p>}
    </div>
  );
}