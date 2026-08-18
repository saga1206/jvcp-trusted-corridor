import { useState } from 'react';
import { generateItinerary } from '../api/resources';

export default function Planner() {
  const [form, setForm] = useState({ destination: '', duration_days: 2, budget_jpy: '', interests: '', preferred_language: 'vi' });
  const [itinerary, setItinerary] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setItinerary(null);
    try {
      const res = await generateItinerary({
        ...form,
        duration_days: Number(form.duration_days),
        budget_jpy: form.budget_jpy ? Number(form.budget_jpy) : null,
      });
      setItinerary(res.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>AI Travel Planner</h1>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 8, maxWidth: 400, marginBottom: 24 }}>
        <input name="destination" placeholder="Destination (e.g. Kyoto)" value={form.destination} onChange={handleChange} required />
        <input name="duration_days" type="number" placeholder="Duration (days)" value={form.duration_days} onChange={handleChange} />
        <input name="budget_jpy" type="number" placeholder="Budget (JPY, optional)" value={form.budget_jpy} onChange={handleChange} />
        <input name="interests" placeholder="Interests (e.g. temples, food)" value={form.interests} onChange={handleChange} />
        <select name="preferred_language" value={form.preferred_language} onChange={handleChange}>
          <option value="vi">Tiếng Việt</option>
          <option value="ja">日本語</option>
          <option value="en">English</option>
        </select>
        <button type="submit" disabled={loading}>{loading ? 'Generating...' : 'Generate Itinerary'}</button>
      </form>

      {itinerary && itinerary.days.map((day) => (
        <div key={day.id} style={{ marginBottom: 20 }}>
          <h3>Day {day.day_number}</h3>
          <p><em>{day.summary}</em></p>
          {day.items.map((item) => (
            <div key={item.id} style={{ borderLeft: '3px solid #6366f1', paddingLeft: 12, marginBottom: 8 }}>
              <strong>{item.time_of_day}: {item.title}</strong>
              <p>{item.description}</p>
              {item.estimated_cost_jpy && <p>Est. cost: ¥{item.estimated_cost_jpy}</p>}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}