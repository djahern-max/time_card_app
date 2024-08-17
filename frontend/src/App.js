import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";
import DailyTimeReport from "./components/DailyTimeReport";
import MechanicsTimeReport from "./components/MechanicsTimeReport";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/daily-time-report" element={<DailyTimeReport />} />
        <Route
          path="/mechanics-time-report"
          element={<MechanicsTimeReport />}
        />
      </Routes>
    </Router>
  );
}

export default App;
