import React from "react";
import { Link } from "react-router-dom";
import "./LandingPage.css"; // We'll define the styles here
import logo from "../assets/1.webp"; // Assuming the logo is in the assets folder

const LandingPage = () => {
  return (
    <div className="landing-container">
      <div className="logo-container">
        <img src={logo} alt="CrewOne2 Logo" className="logo" />
      </div>
      <h1 className="company-name">CrewOne2</h1>
      <div className="links-container">
        <Link to="/register" className="link-button">
          Register
        </Link>
        <Link to="/login" className="link-button">
          Login
        </Link>
      </div>
    </div>
  );
};

export default LandingPage;
