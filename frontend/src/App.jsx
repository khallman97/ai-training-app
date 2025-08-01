import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './auth/LoginPage';
import SignupPage from './auth/SignupPage';
import MainScreen from './main/MainScreen';
import StartPlanPage from './main/StartPlanPage';
import ProfilePage from './main/ProfilePage';
import SettingsPage from './main/SettingsPage';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/main" element={<MainScreen />} />
        <Route path="/start-plan" element={<StartPlanPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
