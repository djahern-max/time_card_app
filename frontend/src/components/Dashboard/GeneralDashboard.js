import React from "react";
import { Link } from "react-router-dom";
import "./AdminDashboard.css"; // Assuming common styling for dashboards

function GeneralDashboard() {
  return (
    <div className="dashboard-container">
      <h1>General Employee Dashboard</h1>
      <ul className="dashboard-menu">
        <li className="dashboard-link">
          <Link to="/general-time-report">Enter Timecard</Link>
        </li>
        <li className="dashboard-link">
          <Link to="/upload-receipt">Upload Receipt</Link>
        </li>
        <li className="dashboard-link">
          <Link to="/schedule">View Schedule</Link>
        </li>
        {/* Add more links as needed */}
      </ul>
    </div>
  );
}

export default GeneralDashboard;
