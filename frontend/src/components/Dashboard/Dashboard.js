import React from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token"); // Clear the token from localStorage
    localStorage.removeItem("role"); // Clear the role from localStorage (optional)
    navigate("/login"); // Redirect to the login page
  };

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <button
        onClick={handleLogout}
        style={{ position: "absolute", top: 10, right: 10 }}
      >
        Logout
      </button>
    </div>
  );
};

export default Dashboard;
