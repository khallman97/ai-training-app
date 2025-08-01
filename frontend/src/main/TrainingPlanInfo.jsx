import React from 'react';
import './TrainingPlanInfo.css';

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};

const formatDuration = (startDate, eventDate) => {
  const start = new Date(startDate);
  const event = new Date(eventDate);
  const days = Math.ceil((event - start) / (1000 * 60 * 60 * 24));
  const weeks = Math.ceil(days / 7);
  return `${weeks} weeks`;
};

const getSkillLevelColor = (skillLevel) => {
  switch (skillLevel.toLowerCase()) {
    case 'beginner': return '#10b981'; // green
    case 'intermediate': return '#f59e0b'; // amber
    case 'master': return '#ef4444'; // red
    default: return '#6b7280'; // gray
  }
};

const getTypeIcon = (type) => {
  switch (type.toLowerCase()) {
    case 'running': return '🏃‍♂️';
    case 'cycling': return '🚴‍♂️';
    case 'triathlon': return '🏊‍♂️';
    default: return '🎯';
  }
};

const formatLongDays = (longDays) => {
  if (!longDays || longDays.length === 0) return 'None';
  return longDays.map(day => 
    day.charAt(0).toUpperCase() + day.slice(1)
  ).join(', ');
};

export default function TrainingPlanInfo({ plan, onUpdateThreshold }) {
  if (!plan) {
    return (
      <div className="training-plan-info">
        <div className="no-plan">
          <div className="no-plan-icon">📋</div>
          <h3>No Active Training Plan</h3>
          <p>Create a training plan to get started with your fitness journey!</p>
        </div>
      </div>
    );
  }

  const daysUntilEvent = Math.ceil((new Date(plan.event_date) - new Date()) / (1000 * 60 * 60 * 24));
  const isEventPassed = daysUntilEvent < 0;
  const isEventToday = daysUntilEvent === 0;

  return (
    <div className="training-plan-info">
      <div className="plan-header">
        <div className="plan-type-icon">
          {getTypeIcon(plan.type)}
        </div>
        <div className="plan-title">
          <h3>{plan.name}</h3>
          <span className="plan-goal">{plan.plan_type}</span>
        </div>
      </div>

      <div className="plan-details">
        <div className="detail-section">
          <h4>Training Schedule</h4>
          <div className="detail-item">
            <span className="detail-label">Start Date:</span>
            <span className="detail-value">{formatDate(plan.start_date)}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Event Date:</span>
            <span className="detail-value">{formatDate(plan.event_date)}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Duration:</span>
            <span className="detail-value">{formatDuration(plan.start_date, plan.event_date)}</span>
          </div>
        </div>

        <div className="detail-section">
          <h4>Event Countdown</h4>
          <div className="countdown">
            {isEventPassed ? (
              <span className="event-passed">Event completed</span>
            ) : isEventToday ? (
              <span className="event-today">Event today!</span>
            ) : (
              <span className="days-remaining">{daysUntilEvent} days remaining</span>
            )}
          </div>
        </div>

        <div className="detail-section">
          <h4>Training Details</h4>
          <div className="detail-item">
            <span className="detail-label">Skill Level:</span>
            <span 
              className="detail-value skill-level"
              style={{ color: getSkillLevelColor(plan.skill_level) }}
            >
              {plan.skill_level}
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Long Days:</span>
            <span className="detail-value">{formatLongDays(plan.long_days)}</span>
          </div>
        </div>

        {plan.description && (
          <div className="detail-section">
            <h4>Description</h4>
            <p className="plan-description">{plan.description}</p>
          </div>
        )}

        {(plan.running_threshold_pace || plan.biking_fpt || plan.critical_swim_speed) && (
          <div className="detail-section">
            <h4>Performance Metrics</h4>
            {plan.running_threshold_pace && (
              <div className="detail-item">
                <span className="detail-label">Running Pace:</span>
                <span className="detail-value">{plan.running_threshold_pace} per km</span>
              </div>
            )}
            {plan.biking_fpt && (
              <div className="detail-item">
                <span className="detail-label">Biking FTP:</span>
                <span className="detail-value">{plan.biking_fpt} watts</span>
              </div>
            )}
            {plan.critical_swim_speed && (
              <div className="detail-item">
                <span className="detail-label">Swim Speed:</span>
                <span className="detail-value">{plan.critical_swim_speed} per 100m</span>
              </div>
            )}
          </div>
        )}

        {plan.additional_data?.custom_distance && (
          <div className="detail-section">
            <h4>Custom Distance</h4>
            <div className="detail-item">
              <span className="detail-value">{plan.additional_data.custom_distance}</span>
            </div>
          </div>
        )}
      </div>

      <div className="plan-actions">
        <button className="btn-edit-plan">Edit Plan</button>
        <button className="btn-update-threshold" onClick={onUpdateThreshold}>Update Threshold</button>
      </div>
    </div>
  );
} 