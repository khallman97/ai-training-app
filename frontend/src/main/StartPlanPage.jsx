import { useNavigate } from 'react-router-dom';

export default function StartPlanPage() {
  const navigate = useNavigate();
  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <button onClick={() => navigate('/main')} style={{ marginBottom: '2rem' }}>&larr; Back</button>
      <h2>Start a Training Plan</h2>
      <p>This is where you will start a new training plan. (Coming soon!)</p>
    </div>
  );
} 