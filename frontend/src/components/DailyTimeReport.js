import React, { useState } from "react";
import axios from "axios";
import "./GeneralTimeReport.css"; // Import the CSS file

function GeneralTimeReport() {
  const [formData, setFormData] = useState({
    name: "",
    date: "",
    hours_worked: "",
    job_name: "",
    description: "",
    equipment: "",
    loads: "",
    pit: "",
    user_id: "", // Assuming the user_id is provided by the logged-in user context
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("http://127.0.0.1:8000/timecards/general", formData)
      .then((response) => console.log(response.data))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="general-form-container">
      <form className="general-form" onSubmit={handleSubmit}>
        <h1>Daily Time Report</h1>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Name"
          className="form-input"
        />
        <input
          type="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          placeholder="Date"
          className="form-input"
        />
        <input
          type="number"
          name="hours_worked"
          value={formData.hours_worked}
          onChange={handleChange}
          placeholder="Hours Worked"
          className="form-input"
        />
        <input
          type="text"
          name="job_name"
          value={formData.job_name}
          onChange={handleChange}
          placeholder="Job Name"
          className="form-input"
        />
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Description"
          className="form-textarea"
        />
        <input
          type="text"
          name="equipment"
          value={formData.equipment}
          onChange={handleChange}
          placeholder="Equipment"
          className="form-input"
        />
        <input
          type="text"
          name="loads"
          value={formData.loads}
          onChange={handleChange}
          placeholder="Loads"
          className="form-input"
        />
        <input
          type="text"
          name="pit"
          value={formData.pit}
          onChange={handleChange}
          placeholder="Pit"
          className="form-input"
        />
        <input
          type="hidden"
          name="user_id"
          value={formData.user_id}
          onChange={handleChange}
          className="form-input"
        />
        <button type="submit" className="form-button">
          Submit
        </button>
      </form>
    </div>
  );
}

export default GeneralTimeReport;
