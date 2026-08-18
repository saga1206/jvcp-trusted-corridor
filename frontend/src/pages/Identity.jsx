import { useEffect, useState } from 'react';
import { getMyProfile, submitVerification } from '../api/resources';

export default function Identity() {
  const [profile, setProfile] = useState(null);
  const [docRef, setDocRef] = useState('');
  const [method, setMethod] = useState('ekyc_document');
  const [message, setMessage] = useState('');

  const load = () => getMyProfile().then((res) => setProfile(res.data));
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await submitVerification({ mock_document_reference: docRef, verification_method: method });
    setMessage('Verification request submitted.');
    setDocRef('');
    load();
  };

  if (!profile) return <p>Loading...</p>;

  return (
    <div>
      <h1>Digital Identity</h1>
      <span className={`stamp ${profile.is_verified ? 'stamp--verified' : 'stamp--pending'}`}>
        {profile.is_verified ? 'Verified' : 'Not verified'}
      </span>
      <p style={{ marginTop: '0.5rem' }}>Preferred language: {profile.preferred_language}</p>

      <h2 style={{ marginTop: '1.5rem' }}>Verifiable Credentials</h2>
      {profile.credentials.length === 0 && <p>None issued yet — approve a verification request via admin to issue one.</p>}
      {profile.credentials.map((c) => (
        <div key={c.credential_id} className="card">
          <p className="mono">{c.credential_id}</p>
          <p>Issuer: <span className="mono">{c.issuer_did}</span></p>
          <p>Subject: <span className="mono">{c.subject_did}</span></p>
          <pre style={{ background: 'var(--cream-deep)', padding: 10, borderRadius: 6, fontSize: '0.8rem' }}>
            {JSON.stringify(c.claims, null, 2)}
          </pre>
        </div>
      ))}

      <h2 style={{ marginTop: '1.5rem' }}>Verification requests</h2>
      {profile.verification_requests.length === 0 && <p>None yet.</p>}
      <ul>
        {profile.verification_requests.map((v) => (
          <li key={v.id}>{v.status} via {v.verification_method} — submitted {new Date(v.submitted_at).toLocaleString()}</li>
        ))}
      </ul>

      <h2 style={{ marginTop: '1.5rem' }}>Submit new verification (mock)</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        <select value={method} onChange={(e) => setMethod(e.target.value)}>
          <option value="ekyc_document">eKYC — Document scan</option>
          <option value="ekyc_selfie">eKYC — Selfie liveness check</option>
          <option value="did_vc_import">Import existing DID/VC</option>
        </select>
        <input placeholder="Mock document reference" value={docRef} onChange={(e) => setDocRef(e.target.value)} />
        <button type="submit">Submit</button>
      </form>
      {message && <p style={{ color: 'var(--sun-red)' }}>{message}</p>}
    </div>
  );
}