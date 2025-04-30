import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const UserForm = ({ setUserId }) => {
  const [form, setForm] = useState({
    id: Math.floor(Math.random() * 10000),
    name: '',
    sport: 'running',
    training_days: [],
    long_days: [],
    goal: '',
    goal_date: '',
    start_date: '',
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleCheckbox = (e, key) => {
    const { value, checked } = e.target;
    const updated = checked
      ? [...form[key], value]
      : form[key].filter((v) => v !== value);
    setForm({ ...form, [key]: updated });
  };

  const handleSubmit = async () => {
    await axios.post('http://localhost:8000/users', form);
    await axios.post(`http://localhost:8000/plans/generate?user_id=${form.id}`);
    setUserId(form.id);
    navigate('/calendar');
  };

  return (
    <div>
      <h2>Training Plan Setup</h2>

      <input
        type="text"
        name="name"
        placeholder="Name"
        onChange={handleChange}
      />

      <select name="sport" onChange={handleChange} value={form.sport}>
        <option value="running">Running</option>
        <option value="biking">Biking</option>
        <option value="triathlon">Triathlon</option>
      </select>

      <input
        type="text"
        name="goal"
        placeholder="Goal (e.g. Half Marathon)"
        onChange={handleChange}
      />

      <label>
        Goal Date:
        <input
          type="date"
          name="goal_date"
          value={form.goal_date}
          onChange={handleChange}
        />
      </label>

      <label>
        Start Date:
        <input
          type="date"
          name="start_date"
          value={form.start_date}
          onChange={handleChange}
        />
      </label>

      <h4>Training Days</h4>
      {["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].map(day => (
        <label key={day}>
          <input
            type="checkbox"
            value={day}
            checked={form.training_days.includes(day)}
            onChange={(e) => handleCheckbox(e, 'training_days')}
          />
          {day}
        </label>
      ))}

      <h4>Long Days</h4>
      {["Saturday", "Sunday"].map(day => (
        <label key={day}>
          <input
            type="checkbox"
            value={day}
            checked={form.long_days.includes(day)}
            onChange={(e) => handleCheckbox(e, 'long_days')}
          />
          {day}
        </label>
      ))}

      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default UserForm;
