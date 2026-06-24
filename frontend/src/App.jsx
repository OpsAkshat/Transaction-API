import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [user, setUser] = useState(null); // { id, name }
  
  // Section 1: Create User
  const [nameInput, setNameInput] = useState('');
  const [isCreatingUser, setIsCreatingUser] = useState(false);
  const [userError, setUserError] = useState(null);

  // Section 2: Submit Transaction
  const [pointsInput, setPointsInput] = useState('');
  const [isSubmittingTx, setIsSubmittingTx] = useState(false);
  const [txMessage, setTxMessage] = useState(null); // { type: 'success' | 'error', text: '' }

  // Section 3: Leaderboard & Summary
  const [rankings, setRankings] = useState([]);
  const [isFetchingRankings, setIsFetchingRankings] = useState(false);
  
  const [summary, setSummary] = useState(null);
  const [isFetchingSummary, setIsFetchingSummary] = useState(false);

  // Fetch rankings on load
  useEffect(() => {
    fetchRankings();
  }, []);

  const handleCreateUser = async (e) => {
    e.preventDefault();
    if (!nameInput.trim()) return;
    setIsCreatingUser(true);
    setUserError(null);
    try {
      const res = await axios.post(`${API_URL}/user`, { name: nameInput });
      setUser({ id: res.data.id, name: res.data.name });
      setNameInput('');
    } catch (err) {
      setUserError(err.response?.data?.detail || err.message);
    } finally {
      setIsCreatingUser(false);
    }
  };

  const handleSubmitTx = async (e) => {
    e.preventDefault();
    if (!pointsInput || isNaN(pointsInput) || Number(pointsInput) <= 0) {
      setTxMessage({ type: 'error', text: 'Please enter a valid points amount greater than 0.' });
      return;
    }
    setIsSubmittingTx(true);
    setTxMessage(null);
    try {
      await axios.post(`${API_URL}/transaction`, {
        user_id: user.id,
        points: Number(pointsInput)
      });
      setTxMessage({ type: 'success', text: 'Transaction submitted successfully!' });
      setPointsInput('');
      fetchRankings(); // Update leaderboard
    } catch (err) {
      setTxMessage({ type: 'error', text: err.response?.data?.detail || err.message });
    } finally {
      setIsSubmittingTx(false);
    }
  };

  const fetchRankings = async () => {
    setIsFetchingRankings(true);
    try {
      const res = await axios.get(`${API_URL}/ranking`);
      setRankings(res.data.rankings || []);
    } catch (err) {
      console.error("Failed to fetch rankings", err);
    } finally {
      setIsFetchingRankings(false);
    }
  };

  const fetchSummary = async () => {
    if (!user) return;
    setIsFetchingSummary(true);
    try {
      const res = await axios.get(`${API_URL}/summary/${user.id}`);
      setSummary(res.data);
    } catch (err) {
      console.error("Failed to fetch summary", err);
    } finally {
      setIsFetchingSummary(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Transaction API</h1>
        <p className="subtitle">Climb the ranks, secure your spot.</p>
      </header>

      <main className="dashboard">
        {/* Section 1 & 2 Container */}
        <div className="actions-grid">
          {/* Section 1: Create User */}
          <section className="card glass-effect">
            <h2>1. Profile</h2>
            {user ? (
              <div className="user-info">
                <div className="avatar">{user.name.charAt(0).toUpperCase()}</div>
                <div>
                  <p className="welcome-text">Welcome back,</p>
                  <p className="user-name">{user.name}</p>
                  <p className="user-id">ID: {user.id}</p>
                </div>
              </div>
            ) : (
              <form onSubmit={handleCreateUser} className="action-form">
                <p className="section-desc">Create a profile to start earning points.</p>
                <div className="input-group">
                  <input
                    type="text"
                    placeholder="Enter your name"
                    value={nameInput}
                    onChange={(e) => setNameInput(e.target.value)}
                    disabled={isCreatingUser}
                  />
                </div>
                {userError && <p className="error-text">{userError}</p>}
                <button type="submit" className="btn-primary" disabled={isCreatingUser || !nameInput.trim()}>
                  {isCreatingUser ? <span className="loader"></span> : 'Create Profile'}
                </button>
              </form>
            )}
          </section>

          {/* Section 2: Submit Transaction */}
          <section className="card glass-effect">
            <h2>2. Submit Points</h2>
            <form onSubmit={handleSubmitTx} className="action-form">
               <p className="section-desc">Add points to climb the leaderboard.</p>
              <div className="input-group">
                <input
                  type="number"
                  placeholder="Points (e.g. 100)"
                  value={pointsInput}
                  onChange={(e) => setPointsInput(e.target.value)}
                  disabled={!user || isSubmittingTx}
                  step="any"
                />
              </div>
              {txMessage && (
                <p className={txMessage.type === 'error' ? 'error-text' : 'success-text'}>
                  {txMessage.text}
                </p>
              )}
              <button
                type="submit"
                className="btn-primary gradient-btn"
                disabled={!user || isSubmittingTx || !pointsInput}
              >
                {isSubmittingTx ? <span className="loader"></span> : 'Submit Transaction'}
              </button>
              {!user && <p className="hint-text">Create a profile first.</p>}
            </form>
          </section>
        </div>

        {/* Section 3: Leaderboard */}
        <section className="card glass-effect full-width">
          <div className="section-header">
            <h2>3. Leaderboard</h2>
            <div className="header-actions">
              <button className="btn-secondary" onClick={fetchRankings} disabled={isFetchingRankings}>
                {isFetchingRankings ? 'Refreshing...' : 'Refresh'}
              </button>
              {user && (
                <button className="btn-outline" onClick={fetchSummary} disabled={isFetchingSummary}>
                  {isFetchingSummary ? 'Loading...' : 'My Summary'}
                </button>
              )}
            </div>
          </div>

          <div className="table-responsive">
            <table className="leaderboard-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Name</th>
                  <th>Total Points</th>
                  <th>Transactions</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {rankings.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="empty-state">No users on the leaderboard yet.</td>
                  </tr>
                ) : (
                  rankings.map((r) => (
                    <tr key={r.user_id} className={r.user_id === user?.id ? 'highlight-row' : ''}>
                      <td className="rank-cell">
                        <span className={`rank-badge rank-${r.rank}`}>{r.rank}</span>
                      </td>
                      <td className="name-cell">{r.name}</td>
                      <td>{r.total_points.toFixed(1)}</td>
                      <td>{r.transaction_count}</td>
                      <td className="score-cell">{r.ranking_Score.toFixed(2)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>

        {/* My Summary Section */}
        {summary && (
          <section className="card glass-effect full-width animate-fade-in">
            <h2>My Summary</h2>
            <div className="summary-stats">
              <div className="stat-box">
                <span className="stat-label">Total Points</span>
                <span className="stat-value">{summary.total_points.toFixed(1)}</span>
              </div>
              <div className="stat-box">
                <span className="stat-label">Transactions</span>
                <span className="stat-value">{summary.transaction_count}</span>
              </div>
            </div>
            
            <h3 className="sub-heading">Transaction History</h3>
            <div className="table-responsive">
              <table className="history-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Points</th>
                    <th>Ref ID</th>
                  </tr>
                </thead>
                <tbody>
                  {summary.transactions.length === 0 ? (
                    <tr>
                      <td colSpan="3" className="empty-state">No transactions yet.</td>
                    </tr>
                  ) : (
                    summary.transactions.map(tx => (
                      <tr key={tx.id}>
                        <td>{new Date(tx.created_at).toLocaleString()}</td>
                        <td className="points-cell">+{tx.points}</td>
                        <td className="ref-cell" title={tx.id}>{tx.id.substring(0, 8)}...</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
