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
        localStorage.setItem("token", response.data.access_token);

        // Assuming the backend sends the role in the response
        const role = response.data.role;
        localStorage.setItem("role", role);

        // Debugging: Log the user role
        console.log("User role:", localStorage.getItem("role"));

        // Debugging: Log the navigation path based on the role
        console.log(
          "Navigating to:",
          role === "admin"
            ? "/dashboard"
            : role === "mechanic"
            ? "/mechanics-time-report"
            : "/daily-time-report"
        );

        // Navigate based on the user's role
        if (role === "admin") {
          navigate("/dashboard");
        } else if (role === "mechanic") {
          navigate("/mechanics-time-report");
        } else if (role === "general") {
          navigate("/daily-time-report");
        } else {
          setError("Unknown user role.");
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
