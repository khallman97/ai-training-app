import React, { useState, useEffect } from 'react';
import './UpdateThresholdModal.css';

export default function UpdateThresholdModal({ isOpen, onClose, onSubmit, currentPlan }) {
  const [formData, setFormData] = useState({
    running_minutes: '',
    running_seconds: '',
    biking_fpt: '',
    swim_minutes: '',
    swim_seconds: ''
  });

  const [errors, setErrors] = useState({});

  // Reset form when modal opens/closes
  useEffect(() => {
    if (isOpen && currentPlan) {
      // Parse existing values if available
      const runningPace = currentPlan.running_threshold_pace;
      const swimSpeed = currentPlan.critical_swim_speed;
      
      if (runningPace) {
        const [minutes, seconds] = runningPace.split(':');
        setFormData(prev => ({
          ...prev,
          running_minutes: minutes || '',
          running_seconds: seconds || ''
        }));
      }
      
      if (swimSpeed) {
        const [minutes, seconds] = swimSpeed.split(':');
        setFormData(prev => ({
          ...prev,
          swim_minutes: minutes || '',
          swim_seconds: seconds || ''
        }));
      }
      
      if (currentPlan.biking_fpt) {
        setFormData(prev => ({
          ...prev,
          biking_fpt: currentPlan.biking_fpt.toString()
        }));
      }
    } else {
      setFormData({
        running_minutes: '',
        running_seconds: '',
        biking_fpt: '',
        swim_minutes: '',
        swim_seconds: ''
      });
      setErrors({});
    }
  }, [isOpen, currentPlan]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

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

    // Validate running pace if provided
    if ((formData.running_minutes || formData.running_seconds) && 
        (!formData.running_minutes || !formData.running_seconds)) {
      newErrors.running_threshold_pace = 'Please enter both minutes and seconds for running pace';
    }

    // Validate swim speed if provided
    if ((formData.swim_minutes || formData.swim_seconds) && 
        (!formData.swim_minutes || !formData.swim_seconds)) {
      newErrors.critical_swim_speed = 'Please enter both minutes and seconds for swim speed';
    }

    // Validate biking FTP if provided
    if (formData.biking_fpt && (isNaN(formData.biking_fpt) || formData.biking_fpt < 0)) {
      newErrors.biking_fpt = 'Must be a positive number';
    }

    // Check if at least one field is filled
    const hasAnyValue = formData.running_minutes || formData.running_seconds || 
                       formData.biking_fpt || formData.swim_minutes || formData.swim_seconds;
    
    if (!hasAnyValue) {
      newErrors.general = 'Please enter at least one threshold value';
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
      running_threshold_pace: formatTime(formData.running_minutes, formData.running_seconds),
      biking_fpt: formData.biking_fpt ? parseInt(formData.biking_fpt) : null,
      critical_swim_speed: formatTime(formData.swim_minutes, formData.swim_seconds)
    };

    try {
      await onSubmit(submitData);
      onClose();
    } catch (error) {
      console.error('Error updating thresholds:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content threshold-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Update Performance Thresholds</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="threshold-form">
          <div className="form-section">
            <p className="form-description">
              Update your performance thresholds. You can update any combination of the fields below.
            </p>
          </div>

          {/* Running Threshold Pace */}
          {(currentPlan?.type === 'Running' || currentPlan?.type === 'Triathlon') && (
            <div className="form-section">
              <h3>Running Threshold Pace</h3>
              <div className="time-input-group">
                <div className="time-inputs">
                  <input
                    type="number"
                    id="running_minutes"
                    name="running_minutes"
                    value={formData.running_minutes}
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
                    value={formData.running_seconds}
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

          {/* Biking FTP */}
          {(currentPlan?.type === 'Cycling' || currentPlan?.type === 'Triathlon') && (
            <div className="form-section">
              <h3>Functional Power Threshold (FTP)</h3>
              <div className="form-group">
                <input
                  type="number"
                  id="biking_fpt"
                  name="biking_fpt"
                  value={formData.biking_fpt}
                  onChange={handleInputChange}
                  placeholder="e.g., 250"
                  className={errors.biking_fpt ? 'error' : ''}
                />
                <span className="input-unit">watts</span>
              </div>
              {errors.biking_fpt && <span className="error-message">{errors.biking_fpt}</span>}
            </div>
          )}

          {/* Critical Swim Speed */}
          {currentPlan?.type === 'Triathlon' && (
            <div className="form-section">
              <h3>Critical Swim Speed</h3>
              <div className="time-input-group">
                <div className="time-inputs">
                  <input
                    type="number"
                    id="swim_minutes"
                    name="swim_minutes"
                    value={formData.swim_minutes}
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
                    value={formData.swim_seconds}
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
          )}

          {errors.general && <span className="error-message general-error">{errors.general}</span>}

          {/* Form Actions */}
          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              Update Thresholds
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 