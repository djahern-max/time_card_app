//Login.js is a component that allows users to log in to the application. It uses the login function from the auth.js file to send a POST request to the backend API with the user's username and password. If the login is successful, the user's token and role are stored in the local storage, and the user is redirected to the appropriate dashboard based on their role.
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../../api/auth";

import "./Login.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await login(username, password);

      if (response.data.access_token) {
        // Clear previous values from localStorage
        localStorage.clear();

        // Store the new token and role in localStorage
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("role", response.data.role); // Store the role

        const role = response.data.role;
        console.log("User role:", role);

        // Navigate based on role
        if (role === "admin") {
          console.log("Navigating to Admin Dashboard");
          navigate("/admin-dashboard");
        } else if (role === "mechanic") {
          console.log("Navigating to Mechanics Dasshboard");
          navigate("/mechanic-dashboard");
        } else {
          console.log("Navigating to Daily Time Report");
          navigate("/general-dashboard");
        }
      }
    } catch (err) {
      setError("Login failed. Please check your username and password.");
    }
  };
  return (
    <div className="container">
      <h1>Login</h1>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleLogin}>
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
        <button type="submit">Login</button>
      </form>
      <p className="register-link">
        Don't have an account yet? <Link to="/register">Register here</Link>
      </p>
    </div>
  );
}

export default Login;
