import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./MechanicsTimeReport.css"; // Import the updated CSS file
import SimpleNavBar from "../Navigation/SimpleNavBar"; // Ensure this path is correct

function MechanicsTimeReport() {
  const [formData, setFormData] = useState({
    name: "",
    date: "",
    hours_worked: "",
    equipment: "",
    equipment_number: "",
    cost_category: "",
    work_order_number: "",
    description: "",
  });

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("http://127.0.0.1:8000/timecards/mechanics", formData)
      .then((response) => {
        console.log(response.data);
        alert("Time card submitted successfully!");
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Failed to submit time card. Please try again.");
      });
  };

  return (
    <div className="general-form-container">
      <SimpleNavBar />

      <form className="general-form" onSubmit={handleSubmit}>
        <h1>Mechanics Time Report</h1>
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
          name="equipment"
          value={formData.equipment}
          onChange={handleChange}
          placeholder="Equipment"
          className="form-input"
        />
        <input
          type="text"
          name="equipment_number"
          value={formData.equipment_number}
          onChange={handleChange}
          placeholder="Equipment Number"
          className="form-input"
        />
        <input
          type="text"
          name="cost_category"
          value={formData.cost_category}
          onChange={handleChange}
          placeholder="Cost Category"
          className="form-input"
        />
        <input
          type="text"
          name="work_order_number"
          value={formData.work_order_number}
          onChange={handleChange}
          placeholder="Work Order Number"
          className="form-input"
        />
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Description"
          className="form-textarea"
        />
        <button type="submit" className="form-button">
          Submit
        </button>
      </form>
    </div>
  );
}

export default MechanicsTimeReport;
