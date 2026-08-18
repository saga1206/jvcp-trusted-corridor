import { useState } from 'react';
import { sendMessage } from '../api/resources';

export default function Assistant() {
  const [threadId, setThreadId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = { role: 'user', content: input };
    setMessages((m) => [...m, userMsg]);
    setInput('');
    setLoading(true);
    try {
      const res = await sendMessage({ thread_id: threadId, message: userMsg.content });
      setThreadId(res.data.thread_id);
      setMessages((m) => [...m, { role: 'assistant', content: res.data.reply }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Multilingual Assistant</h1>
      <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16, minHeight: 300, marginBottom: 12 }}>
        {messages.map((m, i) => (
          <div key={i} style={{ margin: '8px 0', textAlign: m.role === 'user' ? 'right' : 'left' }}>
            <span style={{
              display: 'inline-block', padding: '8px 12px', borderRadius: 12,
              background: m.role === 'user' ? '#6366f1' : '#f3f4f6',
              color: m.role === 'user' ? '#fff' : '#111',
              maxWidth: '80%',
            }}>
              {m.content}
            </span>
          </div>
        ))}
        {loading && <p><em>Assistant is typing...</em></p>}
      </div>
      <form onSubmit={handleSend} style={{ display: 'flex', gap: 8 }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask about travel, payments, refunds..."
          style={{ flex: 1, padding: 8 }} />
        <button type="submit" disabled={loading}>Send</button>
      </form>
    </div>
  );
}