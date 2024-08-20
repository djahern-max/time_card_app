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
        console.log("Fetched data:", data); // Log the data to inspect it

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

  // Helper function to format the amount
  const formatAmount = (amount) => {
    return amount.toLocaleString("en-US", {
      style: "decimal",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  };

  // Helper function to format the job number (removing decimal)
  const formatJob = (job) => {
    return job ? Math.floor(job) : "N/A"; // Use Math.floor to remove decimal
  };

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
          {filteredData.length > 0 ? (
            filteredData.map((entry, index) => (
              <tr key={index}>
                <td>{entry.date}</td>
                <td>{entry.name || "N/A"}</td>
                <td>{formatJob(entry.job)}</td>
                <td>{entry.phase || "N/A"}</td>
                <td>{entry.card_last_four}</td>
                <td>{formatAmount(entry.amount)}</td>
                <td>{entry.description}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="7">No data available</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default HistoricalSchedule;
