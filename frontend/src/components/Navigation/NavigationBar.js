import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./NavigationBar.css";

const NavigationBar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token"); // Adjust according to your auth logic
    navigate("/login"); // Use navigate function instead of history.push
  };

  const handleExport = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Please log in.");
      return;
    }

    try {
      const response = await fetch(
        "http://localhost:8000/export_transactions",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch data for export.");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = "credit_card_transactions.csv"; // The name of the file to download
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);

      alert("Export successful!");
    } catch (error) {
      console.error("Error exporting data:", error);
      alert("There was an error exporting the data. Please try again.");
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">CrewOne2</Link>
      </div>
      <ul className="navbar-links">
        {/* <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/about">About</Link>
        </li>
        <li>
          <Link to="/contact">Contact</Link>
        </li> */}
      </ul>
      <div className="navbar-actions">
        <button className="navbar-logout" onClick={handleLogout}>
          Logout
        </button>
        <button className="navbar-export" onClick={handleExport}>
          Export
        </button>
      </div>
    </nav>
  );
};

export default NavigationBar;
