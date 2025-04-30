import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const localizer = momentLocalizer(moment);

const CalendarView = ({ userId }) => {
  const [events, setEvents] = useState([]);
  const [selectedWorkout, setSelectedWorkout] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/plans/${userId}`).then((res) => {
      const mapped = res.data.map(w => ({
        ...w,
        start: new Date(w.date),
        end: new Date(w.date),
        title: w.title
      }));
      setEvents(mapped);
    });
  }, [userId]);

  const handleSelectEvent = (event) => {
    setSelectedWorkout(event);
  };

  return (
    <div>
      <h2>Your Training Plan</h2>
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 500 }}
        onSelectEvent={handleSelectEvent}
      />

      {selectedWorkout && (
        <div style={{ border: "1px solid #ccc", padding: 10, marginTop: 20 }}>
          <h3>{selectedWorkout.title}</h3>
          <p><strong>Date:</strong> {selectedWorkout.date}</p>
          <p><strong>Duration:</strong> {selectedWorkout.expected_duration}</p>
          <p><strong>Warmup:</strong> {selectedWorkout.warmup}</p>
          <p><strong>Main Set:</strong> {selectedWorkout.main_set}</p>
          <p><strong>Cooldown:</strong> {selectedWorkout.cooldown}</p>
        </div>
      )}
    </div>
  );
};

export default CalendarView;
