//SimpleNavBar.js is a component that provides a simple navigation bar with home and logout icons. It uses Font Awesome icons for the buttons and allows users to navigate to the home page or log out of the application. The component is a reusable navigation bar that can be used across different pages in the application.
import React from "react";
import "./NavigationBar.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faHome, faSignOutAlt } from "@fortawesome/free-solid-svg-icons";
import { useNavigate } from "react-router-dom";

library.add(faHome, faSignOutAlt);

const NavigationBar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="icon-buttons">
        <FontAwesomeIcon
          icon={faHome}
          size="2x"
          onClick={() => navigate("/")}
        />
      </div>
      <ul className="navbar-links"></ul>
      <div className="navbar-actions">
        <FontAwesomeIcon icon={faSignOutAlt} size="2x" onClick={handleLogout} />
      </div>
    </nav>
  );
};

export default NavigationBar;
