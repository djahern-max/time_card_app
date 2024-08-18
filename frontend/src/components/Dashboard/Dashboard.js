import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

function Dashboard() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    axios
      .get(`${API_URL}/users/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        const role = response.data.role;
        if (role === "mechanic") {
          navigate("/mechanics-time-report");
        } else {
          navigate("/daily-time-report");
        }
      })
      .catch((error) => {
        console.error("Error fetching user data", error);
        navigate("/login"); // Redirect to login if there's an error
      });
  }, [navigate]);

  return <div>Loading...</div>;
}

export default Dashboard;
