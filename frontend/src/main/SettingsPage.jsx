import { Link, useNavigate } from 'react-router-dom';
import './MainScreen.css';

export default function SettingsPage() {
  const navigate = useNavigate();

  return (
    <div className="main-content-wrapper">
      <nav className="main-nav">
        <span className="main-logo">AI Training App</span>
        <div className="main-nav-links">
          <Link to="/profile">Profile</Link>
          <Link to="/settings">Settings</Link>
          <button className="main-logout" onClick={() => { localStorage.removeItem('token'); navigate('/login'); }}>Logout</button>
        </div>
      </nav>
      <div className="main-content">
        <div className="main-actions">
          <button className="main-btn" onClick={() => navigate('/main')}>Back to Main</button>
        </div>
        <div className="main-calendar-placeholder">
          <h3>Settings</h3>
          <div className="calendar-empty">
            <p>Settings options will be displayed here.</p>
            <p>This page is under development.</p>
          </div>
        </div>
      </div>
    </div>
  );
} 