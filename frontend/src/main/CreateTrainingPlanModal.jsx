import React, { useState, useEffect } from 'react';
import './CreateTrainingPlanModal.css';

const GOAL_OPTIONS = {
  Triathlon: [
    'sprint',
    'olympic', 
    'half distance',
    'full distance'
  ],
  Running: [
    '5k',
    '10k',
    'Half marathon',
    'Marathon',
    'Ultra'
  ],
  Cycling: [
    'Century',
    'Time trial'
  ]
};

const DAYS_OF_WEEK = [
  'monday', 'tuesday', 'wednesday', 'thursday', 
  'friday', 'saturday', 'sunday'
];

export default function CreateTrainingPlanModal({ isOpen, onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    type: 'Running',
    plan_type: '',
    start_date: '',
    event_date: '',
    skill_level: 'beginner',
    long_days: [],
    running_minutes: '',
    running_seconds: '',
    biking_fpt: '',
    swim_minutes: '',
    swim_seconds: '',
    custom_distance: ''
  });

  const [errors, setErrors] = useState({});
  const [showCustomDistance, setShowCustomDistance] = useState(false);

  // Reset form when modal opens/closes
  useEffect(() => {
    if (isOpen) {
      setFormData({
        name: '',
        description: '',
        type: 'Running',
        plan_type: '',
        start_date: '',
        event_date: '',
        skill_level: 'beginner',
        long_days: [],
        running_minutes: '',
        running_seconds: '',
        biking_fpt: '',
        swim_minutes: '',
        swim_seconds: '',
        custom_distance: ''
      });
      setErrors({});
      setShowCustomDistance(false);
    }
  }, [isOpen]);

  // Show custom distance input for Ultra running or Time trial cycling
  useEffect(() => {
    const needsCustomDistance = 
      (formData.type === 'Running' && formData.plan_type === 'Ultra') ||
      (formData.type === 'Cycling' && formData.plan_type === 'Time trial');
    
    setShowCustomDistance(needsCustomDistance);
  }, [formData.type, formData.plan_type]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (type === 'checkbox') {
      const newLongDays = checked 
        ? [...formData.long_days, value]
        : formData.long_days.filter(day => day !== value);
      
      setFormData(prev => ({
        ...prev,
        long_days: newLongDays
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Required fields
    if (!formData.name.trim()) {
      newErrors.name = 'Plan name is required';
    }

    if (!formData.plan_type) {
      newErrors.plan_type = 'Goal is required';
    }

    if (!formData.start_date) {
      newErrors.start_date = 'Start date is required';
    }

    if (!formData.event_date) {
      newErrors.event_date = 'Event date is required';
    }

    if (formData.start_date && formData.event_date) {
      if (new Date(formData.start_date) >= new Date(formData.event_date)) {
        newErrors.event_date = 'Event date must be after start date';
      }
    }

    if (formData.long_days.length === 0) {
      newErrors.long_days = 'Select at least one day for long training sessions';
    }

    // Custom distance validation
    if (showCustomDistance && !formData.custom_distance.trim()) {
      newErrors.custom_distance = 'Custom distance is required';
    }

    // Optional field format validation
    if ((formData.running_minutes || formData.running_seconds) && 
        (!formData.running_minutes || !formData.running_seconds)) {
      newErrors.running_threshold_pace = 'Please enter both minutes and seconds';
    }

    if ((formData.swim_minutes || formData.swim_seconds) && 
        (!formData.swim_minutes || !formData.swim_seconds)) {
      newErrors.critical_swim_speed = 'Please enter both minutes and seconds';
    }

    if (formData.biking_fpt && (isNaN(formData.biking_fpt) || formData.biking_fpt < 0)) {
      newErrors.biking_fpt = 'Must be a positive number';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    // Format time data
    const formatTime = (minutes, seconds) => {
      if (minutes && seconds) {
        return `${minutes}:${seconds.padStart(2, '0')}`;
      }
      return null;
    };

    // Prepare data for API
    const submitData = {
      name: formData.name,
      description: formData.description,
      type: formData.type,
      plan_type: formData.plan_type,
      start_date: formData.start_date,
      event_date: formData.event_date,
      skill_level: formData.skill_level,
      long_days: formData.long_days,
      running_threshold_pace: formatTime(formData.running_minutes, formData.running_seconds),
      biking_fpt: formData.biking_fpt ? parseInt(formData.biking_fpt) : null,
      critical_swim_speed: formatTime(formData.swim_minutes, formData.swim_seconds),
      additional_data: showCustomDistance ? { custom_distance: formData.custom_distance } : null
    };

    try {
      await onSubmit(submitData);
      onClose();
    } catch (error) {
      console.error('Error creating training plan:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Create Training Plan</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="training-plan-form">
          {/* Basic Information */}
          <div className="form-section">
            <h3>Basic Information</h3>
            
            <div className="form-group">
              <label htmlFor="name">Plan Name *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="e.g., My Marathon Training"
                className={errors.name ? 'error' : ''}
              />
              {errors.name && <span className="error-message">{errors.name}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Optional description of your training plan"
                rows="3"
              />
            </div>
          </div>

          {/* Training Type and Goal */}
          <div className="form-section">
            <h3>Training Type & Goal</h3>
            
            <div className="form-group">
              <label htmlFor="type">Training Type *</label>
              <select
                id="type"
                name="type"
                value={formData.type}
                onChange={handleInputChange}
              >
                <option value="Running">Running</option>
                <option value="Cycling">Cycling</option>
                <option value="Triathlon">Triathlon</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="plan_type">Goal *</label>
              <select
                id="plan_type"
                name="plan_type"
                value={formData.plan_type}
                onChange={handleInputChange}
                className={errors.plan_type ? 'error' : ''}
              >
                <option value="">Select your goal</option>
                {GOAL_OPTIONS[formData.type]?.map(goal => (
                  <option key={goal} value={goal}>{goal}</option>
                ))}
              </select>
              {errors.plan_type && <span className="error-message">{errors.plan_type}</span>}
            </div>

            {showCustomDistance && (
              <div className="form-group">
                <label htmlFor="custom_distance">Distance *</label>
                <input
                  type="text"
                  id="custom_distance"
                  name="custom_distance"
                  value={formData.custom_distance}
                  onChange={handleInputChange}
                  placeholder={formData.type === 'Running' ? 'e.g., 50km, 100km' : 'e.g., 40km, 80km'}
                  className={errors.custom_distance ? 'error' : ''}
                />
                {errors.custom_distance && <span className="error-message">{errors.custom_distance}</span>}
              </div>
            )}
          </div>

          {/* Dates */}
          <div className="form-section">
            <h3>Training Schedule</h3>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="start_date">Start Date *</label>
                <input
                  type="date"
                  id="start_date"
                  name="start_date"
                  value={formData.start_date}
                  onChange={handleInputChange}
                  className={errors.start_date ? 'error' : ''}
                />
                {errors.start_date && <span className="error-message">{errors.start_date}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="event_date">Event Date *</label>
                <input
                  type="date"
                  id="event_date"
                  name="event_date"
                  value={formData.event_date}
                  onChange={handleInputChange}
                  className={errors.event_date ? 'error' : ''}
                />
                {errors.event_date && <span className="error-message">{errors.event_date}</span>}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="skill_level">Skill Level *</label>
              <select
                id="skill_level"
                name="skill_level"
                value={formData.skill_level}
                onChange={handleInputChange}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="master">Master</option>
              </select>
            </div>

            <div className="form-group">
              <label>Long Training Days *</label>
              <div className="checkbox-group">
                {DAYS_OF_WEEK.map(day => (
                  <label key={day} className="checkbox-label">
                    <input
                      type="checkbox"
                      name="long_days"
                      value={day}
                      checked={formData.long_days.includes(day)}
                      onChange={handleInputChange}
                    />
                    <span>{day.charAt(0).toUpperCase() + day.slice(1)}</span>
                  </label>
                ))}
              </div>
              {errors.long_days && <span className="error-message">{errors.long_days}</span>}
            </div>
          </div>

          {/* Performance Metrics (Optional) */}
          <div className="form-section">
            <h3>Performance Metrics (Optional)</h3>
            
            {formData.type === 'Running' && (
              <div className="form-group">
                <label htmlFor="running_threshold_pace">Running Threshold Pace</label>
                <div className="time-input-group">
                  <div className="time-inputs">
                    <input
                      type="number"
                      id="running_minutes"
                      name="running_minutes"
                      value={formData.running_minutes || ''}
                      onChange={handleInputChange}
                      placeholder="5"
                      min="0"
                      max="59"
                      className={errors.running_threshold_pace ? 'error' : ''}
                    />
                    <span className="time-separator">:</span>
                    <input
                      type="number"
                      id="running_seconds"
                      name="running_seconds"
                      value={formData.running_seconds || ''}
                      onChange={handleInputChange}
                      placeholder="00"
                      min="0"
                      max="59"
                      className={errors.running_threshold_pace ? 'error' : ''}
                    />
                  </div>
                  <span className="time-unit">per km</span>
                </div>
                {errors.running_threshold_pace && <span className="error-message">{errors.running_threshold_pace}</span>}
              </div>
            )}

            {formData.type === 'Cycling' && (
              <div className="form-group">
                <label htmlFor="biking_fpt">Functional Power Threshold (FTP)</label>
                <input
                  type="number"
                  id="biking_fpt"
                  name="biking_fpt"
                  value={formData.biking_fpt}
                  onChange={handleInputChange}
                  placeholder="e.g., 250"
                  className={errors.biking_fpt ? 'error' : ''}
                />
                {errors.biking_fpt && <span className="error-message">{errors.biking_fpt}</span>}
              </div>
            )}

            {formData.type === 'Triathlon' && (
              <>
                <div className="form-group">
                  <label htmlFor="running_threshold_pace">Running Threshold Pace</label>
                  <div className="time-input-group">
                    <div className="time-inputs">
                      <input
                        type="number"
                        id="running_minutes"
                        name="running_minutes"
                        value={formData.running_minutes || ''}
                        onChange={handleInputChange}
                        placeholder="5"
                        min="0"
                        max="59"
                        className={errors.running_threshold_pace ? 'error' : ''}
                      />
                      <span className="time-separator">:</span>
                      <input
                        type="number"
                        id="running_seconds"
                        name="running_seconds"
                        value={formData.running_seconds || ''}
                        onChange={handleInputChange}
                        placeholder="00"
                        min="0"
                        max="59"
                        className={errors.running_threshold_pace ? 'error' : ''}
                      />
                    </div>
                    <span className="time-unit">per km</span>
                  </div>
                  {errors.running_threshold_pace && <span className="error-message">{errors.running_threshold_pace}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="biking_fpt">Functional Power Threshold (FTP)</label>
                  <input
                    type="number"
                    id="biking_fpt"
                    name="biking_fpt"
                    value={formData.biking_fpt}
                    onChange={handleInputChange}
                    placeholder="e.g., 250"
                    className={errors.biking_fpt ? 'error' : ''}
                  />
                  {errors.biking_fpt && <span className="error-message">{errors.biking_fpt}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="critical_swim_speed">Critical Swim Speed</label>
                  <div className="time-input-group">
                    <div className="time-inputs">
                      <input
                        type="number"
                        id="swim_minutes"
                        name="swim_minutes"
                        value={formData.swim_minutes || ''}
                        onChange={handleInputChange}
                        placeholder="2"
                        min="0"
                        max="59"
                        className={errors.critical_swim_speed ? 'error' : ''}
                      />
                      <span className="time-separator">:</span>
                      <input
                        type="number"
                        id="swim_seconds"
                        name="swim_seconds"
                        value={formData.swim_seconds || ''}
                        onChange={handleInputChange}
                        placeholder="05"
                        min="0"
                        max="59"
                        className={errors.critical_swim_speed ? 'error' : ''}
                      />
                    </div>
                    <span className="time-unit">per 100m</span>
                  </div>
                  {errors.critical_swim_speed && <span className="error-message">{errors.critical_swim_speed}</span>}
                </div>
              </>
            )}
          </div>

          {/* Form Actions */}
          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              Create Training Plan
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 