import React, { useState, useEffect } from "react";
import "./HistoricalSchedule.css";

function HistoricalSchedule() {
  const [scheduleData, setScheduleData] = useState([]);
  const [employeeNames, setEmployeeNames] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState("");

  // Fetch data on component mount
  useEffect(() => {
    fetch("http://127.0.0.1:8000/combined")
      .then((response) => response.json())
      .then((data) => {
        // Sort data by name
        const sortedData = data.sort((a, b) => a.name.localeCompare(b.name));
        setScheduleData(sortedData);

        // Get unique names for the dropdown
        const names = Array.from(
          new Set(sortedData.map((entry) => entry.name))
        );
        setEmployeeNames(names);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  // Filter data based on selected employee
  const filteredData = selectedEmployee
    ? scheduleData.filter((entry) => entry.name === selectedEmployee)
    : scheduleData;

  return (
    <div className="historical-schedule-container">
      <h1>Credit Card Transactions</h1>

      <div className="filter-container">
        <label htmlFor="employee-select">Filter by Employee:</label>
        <select
          id="employee-select"
          value={selectedEmployee}
          onChange={(e) => setSelectedEmployee(e.target.value)}
        >
          <option value="">All Employees</option>
          {employeeNames.map((name, index) => (
            <option key={index} value={name}>
              {name}
            </option>
          ))}
        </select>
      </div>

      <table className="historical-schedule-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Name</th>
            <th>Job</th>
            <th>Phase</th>
            <th>Card Last Four</th>
            <th>Amount</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((entry, index) => (
            <tr key={index}>
              <td>{entry.date}</td>
              <td>{entry.name}</td>
              <td>{entry.job}</td>
              <td>{entry.phase}</td>
              <td>{entry.card_last_four}</td>
              <td>{entry.amount}</td>
              <td>{entry.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HistoricalSchedule;
