import React, { useState } from "react";
import axios from "axios";

function DailyTimeReport() {
  const [formData, setFormData] = useState({
    name: "",
    date: "",
    hours_worked: "",
    job_name: "",
    description: "",
    equipment: "",
    loads: "",
    pit: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("http://127.0.0.1:8000/timecards/daily", formData)
      .then((response) => console.log(response.data))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Render fields similar to the daily time report */}
      {/* Example */}
      <input
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="Name"
      />
      {/* Add other fields here */}
      <button type="submit">Submit</button>
    </form>
  );
}

export default DailyTimeReport;
