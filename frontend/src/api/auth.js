import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export const login = (username, password) => {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  return axios.post(`${API_URL}/login`, formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};

export const register = (username, password) => {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  return axios.post(`${API_URL}/register`, formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};
