import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";
import DailyTimeReport from "./components/DailyTimeReport";
import MechanicsTimeReport from "./components/MechanicsTimeReport";
import Upload from "./components/Upload"; // Import the new Upload component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/daily-time-report" element={<DailyTimeReport />} />
        <Route
          path="/mechanics-time-report"
          element={<MechanicsTimeReport />}
        />
        <Route path="/upload" element={<Upload />} /> {/* Add the new route */}
      </Routes>
    </Router>
  );
}

export default App;
