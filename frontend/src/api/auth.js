import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export const login = (username, password) => {
  const loginData = {
    username,
    password,
  };

  return axios.post(`${API_URL}/login`, loginData, {
    headers: {
      "Content-Type": "application/json",
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
