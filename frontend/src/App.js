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

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={role === "admin" ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route
          path="/daily-time-report"
          element={
            role === "general" ? <DailyTimeReport /> : <Navigate to="/login" />
          }
        />
        <Route
          path="/mechanics-time-report"
          element={
            role === "mechanic" ? (
              <MechanicsTimeReport />
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route path="/upload" element={<Upload />} />
      </Routes>
    </Router>
  );
}

export default App;
