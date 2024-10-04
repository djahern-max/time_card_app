// auth.js is a file that contains functions to interact with the backend authentication API endpoints.
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export const login = (username, password) => {
  const data = new URLSearchParams();
  data.append("username", username);
  data.append("password", password);

  return axios.post("http://127.0.0.1:8000/login", data, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};
export const getCurrentUser = () => {
  const token = localStorage.getItem("token");
  return axios.get("http://127.0.0.1:8000/users/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const register = (username, password, role) => {
  return axios.post(
    `${API_URL}/register`,
    { username, password, role }, // Sending as JSON
    {
      headers: {
        "Content-Type": "application/json", // Using JSON content type
      },
    }
  );
};
