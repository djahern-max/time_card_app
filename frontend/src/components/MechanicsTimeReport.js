import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function MechanicsTimeReport() {
  const [formData, setFormData] = useState({
    date: "",
    name: "",
    equipmentUsed: "",
    costCode: "",
    workOrder: "",
    description: "",
    totalHours: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/timecards/mechanics",
        formData
      );
      if (response.status === 200) {
        navigate("/success");
      }
    } catch (err) {
      setError("Failed to submit the report. Please try again.");
    }
  };

  return (
    <div className="container">
      <h1>Mechanics Time Report</h1>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="date">Date</label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="equipmentUsed">Equipment Used</label>
          <input
            type="text"
            id="equipmentUsed"
            name="equipmentUsed"
            value={formData.equipmentUsed}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="costCode">Cost Code</label>
          <input
            type="text"
            id="costCode"
            name="costCode"
            value={formData.costCode}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="workOrder">Work Order #</label>
          <input
            type="text"
            id="workOrder"
            name="workOrder"
            value={formData.workOrder}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="totalHours">Total Hours</label>
          <input
            type="number"
            id="totalHours"
            name="totalHours"
            value={formData.totalHours}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default MechanicsTimeReport;
