import React, { useState, useEffect } from "react";
// import "./AllEmployeesSchedule.css";

function AllEmployeesSchedule() {
  const [date, setDate] = useState("");
  const [schedules, setSchedules] = useState([]);

  useEffect(() => {
    if (date) {
      fetch(`http://127.0.0.1:8000/schedule?date=${date}`)
        .then((response) => response.json())
        .then((data) => {
          setSchedules(data);
        })
        .catch((error) => console.error("Error fetching schedules:", error));
    }
  }, [date]);

  return (
    <div className="all-employees-schedule-container">
      <h1>All Employees' Schedule</h1>

      <div className="filter-container">
        <label htmlFor="schedule-date">Select Date:</label>
        <input
          type="date"
          id="schedule-date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>

      {schedules.length === 0 ? (
        <div>No schedules found for {date}.</div>
      ) : (
        <table className="schedule-table">
          <thead>
            <tr>
              <th>Employee Code</th>
              <th>Date</th>
              <th>Job</th>
              <th>Phase</th>
            </tr>
          </thead>
          <tbody>
            {schedules.map((schedule, index) => (
              <tr key={index}>
                <td>{schedule.emp_code}</td>
                <td>{schedule.date}</td>
                <td>{schedule.job || "N/A"}</td>
                <td>{schedule.phase || "N/A"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default AllEmployeesSchedule;
