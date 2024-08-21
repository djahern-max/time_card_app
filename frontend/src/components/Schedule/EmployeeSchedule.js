import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
// import "./EmployeeSchedule.css";

function EmployeeSchedule() {
  const { emp_code, date } = useParams(); // Assuming you navigate to this component with emp_code and date params
  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/schedule/${emp_code}/${date}`)
      .then((response) => response.json())
      .then((data) => {
        setSchedule(data);
      })
      .catch((error) => console.error("Error fetching schedule:", error));
  }, [emp_code, date]);

  if (schedule.length === 0) {
    return (
      <div>
        No schedule found for {emp_code} on {date}.
      </div>
    );
  }

  return (
    <div className="schedule-container">
      <h1>
        Schedule for {emp_code} on {date}
      </h1>
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
          {schedule.map((entry, index) => (
            <tr key={index}>
              <td>{entry.emp_code}</td>
              <td>{entry.date}</td>
              <td>{entry.job || "N/A"}</td>
              <td>{entry.phase || "N/A"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EmployeeSchedule;
