// Register.js is a component that allows users to register for an account. It includes a form with fields for username, password, and role. The user can select their role from a dropdown menu with options for "General Employee" and "Mechanic". The component also includes error handling for registration failures and a link to the login page for users who already have an account.
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../../api/auth";
import "./Register.css";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("general"); // Default to 'general'
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      // Make sure the username and password are not empty
      if (!username || !password) {
        setError("Username and password are required");
        return;
      }

      const response = await register(username, password, role);
      if (response.data.id) {
        navigate("/login");
      }
    } catch (err) {
      setError("Registration failed. Please try again.");
    }
  };

  return (
    <div className="container">
      <h1>Register</h1>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleRegister}>
        <div>
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="role">Role</label>
          <select
            id="role"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            required
          >
            <option value="general">General Employee</option>
            <option value="mechanic">Mechanic</option>
          </select>
        </div>
        <button type="submit">Register</button>
      </form>
      <p className="login-link">
        Already have an account? <Link to="/login">Login here</Link>
      </p>
    </div>
  );
}

export default Register;
