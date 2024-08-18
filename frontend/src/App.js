import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import LandingPage from "./components/LandingPage/LandingPage";
import Login from "./components/Authentication/Login";
import Register from "./components/Authentication/Register";
import Dashboard from "./components/Dashboard/Dashboard";
import DailyTimeReport from "./components/TimeReports/DailyTimeReport";
import MechanicsTimeReport from "./components/TimeReports/MechanicsTimeReport";
import Upload from "./components/Upload/Upload";

function App() {
  const role = localStorage.getItem("role");

  console.log("App role:", role); // Debugging line

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
        <Route path="/upload" element={<Upload />} />
      </Routes>
    </Router>
  );
}

export default App;
