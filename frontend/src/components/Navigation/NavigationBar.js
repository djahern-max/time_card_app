import React from "react";
import "./NavigationBar.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faHome,
  faSignOutAlt,
  faFileExport,
} from "@fortawesome/free-solid-svg-icons";
import { useNavigate } from "react-router-dom";

library.add(faHome, faSignOutAlt, faFileExport);

const NavigationBar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
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
      <div className="icon-buttons">
        <FontAwesomeIcon
          icon={faHome}
          size="2x"
          onClick={() => navigate("/home")}
        />
      </div>
      <ul className="navbar-links"></ul>
      <div className="navbar-actions">
        <FontAwesomeIcon icon={faFileExport} size="2x" onClick={handleExport} />
        <FontAwesomeIcon icon={faSignOutAlt} size="2x" onClick={handleLogout} />
      </div>
    </nav>
  );
};

export default NavigationBar;
