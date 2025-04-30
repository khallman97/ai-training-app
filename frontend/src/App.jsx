import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import UserForm from './UserForm';
import CalendarView from './CalendarView';

const App = () => {
  const [userId, setUserId] = useState(null);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<UserForm setUserId={setUserId} />} />
        <Route path="/calendar" element={userId ? <CalendarView userId={userId} /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;
