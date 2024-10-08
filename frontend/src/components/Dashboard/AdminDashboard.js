// AdminDashboard.js
import React from "react";
import { Link } from "react-router-dom";
import "./AdminDashboard.css";

function Dashboard() {
  return (
    <div className="dashboard-container">
      <h1>Admin Dashboard</h1>
      <div className="dashboard-links">
        <Link to="/upload" className="dashboard-link">
          Upload Data
        </Link>
        <Link to="/credit-card-transactions" className="dashboard-link">
          Review Credit Card Transactions
        </Link>
        <Link to="/all-employees-schedule" className="dashboard-link">
          View All Employees' Schedule
        </Link>
        <Link to="/bulk-receipt-upload" className="dashboard-link">
          Bulk Receipt Upload
        </Link>
      </div>
      <div className="dashboard-logout">
        <button
          onClick={() => {
            localStorage.clear();
            window.location.href = "/login";
          }}
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
