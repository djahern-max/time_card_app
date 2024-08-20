import React from "react";
import { Link } from "react-router-dom";
import "./Dashboard.css";

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
