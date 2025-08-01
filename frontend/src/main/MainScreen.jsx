import { Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import CreateTrainingPlanModal from './CreateTrainingPlanModal';
import UpdateThresholdModal from './UpdateThresholdModal';
import TrainingPlanInfo from './TrainingPlanInfo';
import './MainScreen.css';

export default function MainScreen() {
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);
  const [showThresholdModal, setShowThresholdModal] = useState(false);
  const [hasActivePlan, setHasActivePlan] = useState(false);
  const [activePlan, setActivePlan] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check if user has an active training plan
  useEffect(() => {
    checkTrainingPlanStatus();
  }, []);

  const checkTrainingPlanStatus = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      const response = await fetch('http://localhost:8000/training-plans/status', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setHasActivePlan(data.has_active_plan);
        setActivePlan(data.active_plan);
      }
    } catch (error) {
      console.error('Error checking training plan status:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTrainingPlan = async (planData) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      const response = await fetch('http://localhost:8000/training-plans/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(planData)
      });

      if (response.ok) {
        const newPlan = await response.json();
        console.log('Training plan created:', newPlan);
        setHasActivePlan(true);
        setActivePlan(newPlan);
        // You could show a success message here
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create training plan');
      }
    } catch (error) {
      console.error('Error creating training plan:', error);
      alert('Failed to create training plan: ' + error.message);
      throw error;
    }
  };

  const handleStartPlanClick = () => {
    // Open the modal to create a new plan
    setShowModal(true);
  };

  const handleUpdateThreshold = () => {
    setShowThresholdModal(true);
  };

  const handleUpdateThresholdSubmit = async (thresholdData) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      // Update the active plan with new thresholds
      const response = await fetch(`http://localhost:8000/training-plans/${activePlan.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(thresholdData)
      });

      if (response.ok) {
        const updatedPlan = await response.json();
        setActivePlan(updatedPlan);
        // You could show a success message here
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update thresholds');
      }
    } catch (error) {
      console.error('Error updating thresholds:', error);
      alert('Failed to update thresholds: ' + error.message);
      throw error;
    }
  };

  if (loading) {
    return (
      <div className="main-content-wrapper">
        <div className="main-content">
          <div className="loading">Loading...</div>
        </div>
      </div>
    );
  }

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
        <div className="main-layout">
          {/* Left Sidebar - Training Plan Info */}
          <div className="main-sidebar">
            <TrainingPlanInfo 
              plan={activePlan} 
              onUpdateThreshold={handleUpdateThreshold}
            />
          </div>
          
          {/* Center - Calendar Area */}
          <div className="main-center">
            {!hasActivePlan && (
              <div className="main-actions">
                <button 
                  className="main-btn" 
                  onClick={handleStartPlanClick}
                >
                  Start Training Plan
                </button>
              </div>
            )}
            <div className="main-calendar-placeholder">
              <h3>Calendar View</h3>
              <div className="calendar-empty">
                {hasActivePlan ? 'Your training plan will appear here.' : 'No training plan yet.'}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Training Plan Creation Modal */}
      <CreateTrainingPlanModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        onSubmit={handleCreateTrainingPlan}
      />

      {/* Update Threshold Modal */}
      <UpdateThresholdModal
        isOpen={showThresholdModal}
        onClose={() => setShowThresholdModal(false)}
        onSubmit={handleUpdateThresholdSubmit}
        currentPlan={activePlan}
      />
    </div>
  );
} 